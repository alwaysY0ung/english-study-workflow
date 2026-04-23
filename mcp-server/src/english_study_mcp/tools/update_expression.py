"""기존 시트의 특정 행을 수정하는 툴."""
from __future__ import annotations

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "update_expression",
    "description": (
        "시트의 기존 행을 업데이트합니다. 이미 저장된 표현에 예문을 추가하거나, "
        "잘못 기록된 내용을 수정할 때 사용합니다. 두 가지 방식 지원: "
        "(1) row_number 직접 지정 "
        "(2) find_by_column + find_by_value 로 먼저 찾기. "
        "사용자가 '방금 저장한 X의 예문 추가해줘' / 'Y행 수정' 등으로 요청 시 사용하세요."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "sheet": {
                "type": "string",
                "description": "시트 별명",
            },
            "updates": {
                "type": "object",
                "description": (
                    "수정할 컬럼과 값 (키: 컬럼명/별칭, 값: 새 값). "
                    "예: {\"example3\": \"Can I pick your brain over coffee?\", "
                    "\"note\": \"매우 캐주얼한 요청\"}"
                ),
                "additionalProperties": {"type": "string"},
            },
            "row_number": {
                "type": "integer",
                "description": "수정할 행 번호 (헤더가 1행, 데이터는 2부터). 없으면 find_by_* 사용.",
            },
            "find_by_column": {
                "type": "string",
                "description": "행을 찾을 기준 컬럼 (예: 'expression')",
            },
            "find_by_value": {
                "type": "string",
                "description": "기준 컬럼에서 일치해야 할 값",
            },
        },
        "required": ["sheet", "updates"],
    },
}


def run(
    client: SheetsClient,
    sheet: str,
    updates: dict[str, str],
    row_number: int | None = None,
    find_by_column: str | None = None,
    find_by_value: str | None = None,
) -> str:
    schema = client.registry.get_sheet(sheet)

    if row_number is None:
        if not (find_by_column and find_by_value):
            return "❌ row_number 또는 (find_by_column + find_by_value) 중 하나는 필요합니다."
        found = client.find_row_by_key(schema, find_by_column, find_by_value)
        if found is None:
            return f"❌ '{schema.tab_name}' 시트에서 {find_by_column}='{find_by_value}' 인 행을 찾지 못했습니다."
        row_number, _ = found

    mapped = client.update_row(schema, row_number, updates)

    lines = [f"✅ '{schema.tab_name}' 시트 {row_number}행 업데이트."]
    for key, value in mapped.items():
        display = value if len(value) <= 80 else value[:77] + "..."
        lines.append(f"  • {key}: {display}")
    return "\n".join(lines)
