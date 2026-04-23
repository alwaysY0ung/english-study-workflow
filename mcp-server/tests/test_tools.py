"""새 툴들의 정의가 올바른지 검증 (API 호출 없음)."""
from __future__ import annotations

from english_study_mcp.server import TOOLS


def test_all_8_tools_registered() -> None:
    expected = {
        "add_expression",
        "search_expressions",
        "list_sheets",
        "quiz_random",
        "correct_expression",
        "add_translation_row",
        "update_expression",
        "weekly_review",
    }
    assert set(TOOLS.keys()) == expected


def test_tool_definitions_have_required_fields() -> None:
    for name, (defn, _) in TOOLS.items():
        assert defn["name"] == name
        assert "description" in defn
        assert "inputSchema" in defn
        assert defn["inputSchema"]["type"] == "object"


def test_correct_expression_required_fields() -> None:
    defn, _ = TOOLS["correct_expression"]
    required = defn["inputSchema"].get("required", [])
    assert "my_version" in required
    assert "corrected" in required


def test_update_expression_flexible_inputs() -> None:
    defn, _ = TOOLS["update_expression"]
    required = defn["inputSchema"].get("required", [])
    # sheet와 updates만 필수. row_number나 find_by_* 는 런타임에 판별.
    assert required == ["sheet", "updates"]


def test_weekly_review_has_no_required() -> None:
    defn, _ = TOOLS["weekly_review"]
    # 전부 선택사항 (기본값 있음)
    assert defn["inputSchema"].get("required", []) == []


def test_add_translation_row_minimum() -> None:
    defn, _ = TOOLS["add_translation_row"]
    required = defn["inputSchema"].get("required", [])
    # original만 필수 (my_try/correct_translation 없이도 저장 가능)
    assert required == ["original"]
