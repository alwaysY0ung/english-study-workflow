"""시트 스키마 레지스트리 로더."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml


@dataclass
class ColumnSchema:
    name: str
    aliases: list[str] = field(default_factory=list)
    required: bool = False
    auto_fill: str | None = None  # "today" 등

    def matches(self, key: str) -> bool:
        k = key.lower().strip()
        if k == self.name.lower():
            return True
        return any(k == a.lower() for a in self.aliases)

    def auto_value(self) -> str | None:
        if self.auto_fill == "today":
            return date.today().isoformat()
        return None


@dataclass
class SheetSchema:
    alias: str
    tab_name: str
    columns: list[ColumnSchema]

    def column_names(self) -> list[str]:
        return [c.name for c in self.columns]

    def find_column(self, key: str) -> ColumnSchema | None:
        for col in self.columns:
            if col.matches(key):
                return col
        return None


@dataclass
class Registry:
    spreadsheet_id: str
    sheets: dict[str, SheetSchema]

    def get_sheet(self, alias: str) -> SheetSchema:
        a = alias.lower().strip()
        if a not in self.sheets:
            available = ", ".join(self.sheets.keys())
            raise KeyError(f"'{alias}' 시트를 찾을 수 없음. 가능한 시트: {available}")
        return self.sheets[a]


def load_registry(path: str | Path | None = None) -> Registry:
    """YAML 파일에서 스키마 로드."""
    if path is None:
        path = os.environ.get("ENGLISH_STUDY_CONFIG")
    if not path:
        raise ValueError(
            "시트 레지스트리 경로가 지정되지 않았습니다. "
            "ENGLISH_STUDY_CONFIG 환경변수를 설정하세요."
        )

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"레지스트리 파일이 없습니다: {p}")

    data = yaml.safe_load(p.read_text())

    sheets: dict[str, SheetSchema] = {}
    for alias, spec in (data.get("sheets") or {}).items():
        columns = [
            ColumnSchema(
                name=c["name"],
                aliases=c.get("aliases", []),
                required=c.get("required", False),
                auto_fill=c.get("auto_fill"),
            )
            for c in spec.get("columns", [])
        ]
        sheets[alias.lower()] = SheetSchema(
            alias=alias,
            tab_name=spec["tab_name"],
            columns=columns,
        )

    return Registry(
        spreadsheet_id=data["spreadsheet_id"],
        sheets=sheets,
    )
