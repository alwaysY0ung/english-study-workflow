"""스키마 레지스트리 테스트 (Google API 호출 없음)."""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from english_study_mcp.schemas.registry import ColumnSchema, load_registry


@pytest.fixture
def registry_yaml(tmp_path: Path) -> Path:
    content = """
spreadsheet_id: "test-id-123"
sheets:
  business:
    tab_name: "Business"
    columns:
      - name: expression
        aliases: ["phrase", "표현"]
        required: true
      - name: meaning_kr
        required: true
      - name: date
        auto_fill: today
  daily:
    tab_name: "Daily"
    columns:
      - name: expression
      - name: example
"""
    p = tmp_path / "registry.yaml"
    p.write_text(content)
    return p


def test_load_registry(registry_yaml: Path) -> None:
    registry = load_registry(registry_yaml)
    assert registry.spreadsheet_id == "test-id-123"
    assert set(registry.sheets.keys()) == {"business", "daily"}


def test_get_sheet(registry_yaml: Path) -> None:
    registry = load_registry(registry_yaml)
    sheet = registry.get_sheet("business")
    assert sheet.tab_name == "Business"
    assert len(sheet.columns) == 3


def test_get_sheet_not_found(registry_yaml: Path) -> None:
    registry = load_registry(registry_yaml)
    with pytest.raises(KeyError):
        registry.get_sheet("nonexistent")


def test_column_alias_matching() -> None:
    col = ColumnSchema(name="expression", aliases=["phrase", "표현"])
    assert col.matches("expression")
    assert col.matches("phrase")
    assert col.matches("표현")
    assert col.matches("EXPRESSION")  # case insensitive
    assert not col.matches("meaning")


def test_auto_fill_today() -> None:
    col = ColumnSchema(name="date", auto_fill="today")
    assert col.auto_value() == date.today().isoformat()


def test_find_column(registry_yaml: Path) -> None:
    registry = load_registry(registry_yaml)
    sheet = registry.get_sheet("business")
    assert sheet.find_column("phrase").name == "expression"
    assert sheet.find_column("표현").name == "expression"
    assert sheet.find_column("unknown") is None
