"""gspread를 감싼 시트 클라이언트."""
from __future__ import annotations

import gspread
from gspread.exceptions import WorksheetNotFound

from .auth import get_credentials
from .schemas.registry import Registry, SheetSchema


class SheetsClient:
    def __init__(self, registry: Registry):
        self.registry = registry
        self._gc = gspread.authorize(get_credentials())
        self._spreadsheet = self._gc.open_by_key(registry.spreadsheet_id)

    def _worksheet(self, schema: SheetSchema) -> gspread.Worksheet:
        try:
            return self._spreadsheet.worksheet(schema.tab_name)
        except WorksheetNotFound:
            raise ValueError(
                f"탭 '{schema.tab_name}' 이 스프레드시트에 없습니다. "
                f"Google Sheets에서 먼저 탭을 만들고 1행에 헤더를 입력하세요."
            )

    def get_header(self, schema: SheetSchema) -> list[str]:
        ws = self._worksheet(schema)
        return ws.row_values(1)

    def append_row(
        self, schema: SheetSchema, data: dict[str, str]
    ) -> tuple[int, dict[str, str]]:
        """데이터를 시트 구조에 맞게 매핑해 새 행 추가.

        Returns:
            (row_number, mapped_data)
        """
        ws = self._worksheet(schema)
        header = ws.row_values(1)

        if not header:
            # 헤더가 없으면 스키마 기준으로 생성
            header = schema.column_names()
            ws.update("1:1", [header])

        # data 키를 스키마 컬럼명으로 정규화
        mapped: dict[str, str] = {}
        for key, value in data.items():
            col = schema.find_column(key)
            if col is None:
                # 스키마에 없는 키는 무시 (헤더에 있으면 그대로 사용)
                if key in header:
                    mapped[key] = value
                continue
            mapped[col.name] = value

        # auto_fill 적용
        for col in schema.columns:
            if col.name not in mapped:
                auto = col.auto_value()
                if auto is not None:
                    mapped[col.name] = auto

        # 필수 컬럼 체크
        missing = [c.name for c in schema.columns if c.required and not mapped.get(c.name)]
        if missing:
            raise ValueError(f"필수 컬럼 누락: {missing}")

        # 헤더 순서대로 행 구성
        row = [mapped.get(h, "") for h in header]
        ws.append_row(row, value_input_option="USER_ENTERED")

        row_number = len(ws.get_all_values())
        return row_number, mapped

    def search(
        self,
        schema: SheetSchema,
        query: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, str]]:
        """시트에서 query와 부분일치하는 행 반환 (query가 None이면 최근 N개)."""
        ws = self._worksheet(schema)
        records = ws.get_all_records()

        if query:
            q = query.lower().strip()
            records = [r for r in records if any(q in str(v).lower() for v in r.values())]

        # 최근 것부터
        return list(reversed(records))[:limit]

    def random_sample(self, schema: SheetSchema, count: int = 10) -> list[dict[str, str]]:
        import random

        ws = self._worksheet(schema)
        records = ws.get_all_records()
        if not records:
            return []
        count = min(count, len(records))
        return random.sample(records, count)

    def sheet_info(self, schema: SheetSchema) -> dict:
        ws = self._worksheet(schema)
        values = ws.get_all_values()
        return {
            "alias": schema.alias,
            "tab_name": schema.tab_name,
            "columns": schema.column_names(),
            "row_count": max(len(values) - 1, 0),  # 헤더 제외
        }

    # ========== 추가 툴에서 사용할 메서드 ==========

    def update_row(
        self, schema: SheetSchema, row_number: int, updates: dict[str, str]
    ) -> dict[str, str]:
        """특정 행의 일부 셀만 업데이트.

        row_number는 1-based (헤더 제외하면 2부터 시작).
        """
        ws = self._worksheet(schema)
        header = ws.row_values(1)

        mapped: dict[str, str] = {}
        for key, value in updates.items():
            col = schema.find_column(key)
            if col is None:
                if key in header:
                    mapped[key] = value
                continue
            mapped[col.name] = value

        # 실제 셀 업데이트
        for col_name, value in mapped.items():
            if col_name not in header:
                continue
            col_idx = header.index(col_name) + 1  # 1-based
            ws.update_cell(row_number, col_idx, value)

        return mapped

    def find_row_by_key(
        self, schema: SheetSchema, key_column: str, key_value: str
    ) -> tuple[int, dict[str, str]] | None:
        """특정 컬럼의 값으로 행을 찾아 (행번호, 데이터) 반환."""
        col = schema.find_column(key_column)
        if col is None:
            raise ValueError(f"컬럼을 찾을 수 없음: {key_column}")

        ws = self._worksheet(schema)
        records = ws.get_all_records()
        needle = key_value.lower().strip()

        for i, record in enumerate(records, start=2):  # 헤더가 1행
            if str(record.get(col.name, "")).lower().strip() == needle:
                return i, record
        return None

    def filter_by_date_range(
        self,
        schema: SheetSchema,
        days: int = 7,
        date_column: str = "date",
    ) -> list[dict[str, str]]:
        """최근 N일 이내 행 반환 (date 컬럼이 있는 시트용)."""
        from datetime import date, timedelta

        col = schema.find_column(date_column)
        if col is None:
            return []  # date 컬럼 없으면 필터 불가

        cutoff = date.today() - timedelta(days=days)
        ws = self._worksheet(schema)
        records = ws.get_all_records()

        filtered = []
        for record in records:
            date_str = str(record.get(col.name, "")).strip()
            if not date_str:
                continue
            try:
                # ISO 포맷 (2026-04-22)
                row_date = date.fromisoformat(date_str[:10])
                if row_date >= cutoff:
                    filtered.append(record)
            except ValueError:
                continue
        return filtered

    def all_records(self, schema: SheetSchema) -> list[dict[str, str]]:
        """시트의 모든 행을 dict 리스트로 반환."""
        ws = self._worksheet(schema)
        return ws.get_all_records()
