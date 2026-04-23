"""주간/기간별 학습 요약 데이터를 반환하는 툴."""
from __future__ import annotations

import json

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "weekly_review",
    "description": (
        "지정한 기간(기본 7일) 동안의 학습 기록을 여러 시트에서 수집해 반환합니다. "
        "Claude는 반환된 데이터를 바탕으로 요약/패턴 분석/학습 인사이트를 직접 제공하세요. "
        "예: '이번 주 뭐 배웠어?' / '지난 2주 복습' 등의 요청에 사용."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "description": "조회할 기간 (일 단위, 기본 7)",
                "default": 7,
            },
            "sheets": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "조회할 시트 별명 리스트 (선택). 없으면 date 컬럼이 있는 모든 시트. "
                    "예: ['daily', 'corrections']"
                ),
            },
        },
    },
}


def run(
    client: SheetsClient,
    days: int = 7,
    sheets: list[str] | None = None,
) -> str:
    target_sheets = sheets or list(client.registry.sheets.keys())

    result: dict[str, list[dict]] = {}
    for alias in target_sheets:
        try:
            schema = client.registry.get_sheet(alias)
        except KeyError:
            continue
        # date 컬럼 없는 시트는 스킵
        if not schema.find_column("date"):
            continue
        rows = client.filter_by_date_range(schema, days=days)
        if rows:
            result[alias] = rows

    summary = {
        "period_days": days,
        "totals": {alias: len(rows) for alias, rows in result.items()},
        "data": result,
    }
    return json.dumps(summary, ensure_ascii=False, indent=2)
