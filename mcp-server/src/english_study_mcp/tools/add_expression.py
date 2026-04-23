"""영어 표현을 시트에 추가하는 툴."""
from __future__ import annotations

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "add_expression",
    "description": (
        "영어 표현·뜻·예문 등을 지정된 시트에 새 행으로 추가합니다. "
        "시트 구조는 registry.yaml에 정의된 컬럼 별칭을 자동으로 매핑하며, "
        "date 등 auto_fill 컬럼은 자동 채워집니다. "
        "사용자가 '시트에 정리/저장/기록해줘'라고 말할 때 사용하세요."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "sheet": {
                "type": "string",
                "description": "시트 별명 (예: business, daily, phrasal_verbs)",
            },
            "data": {
                "type": "object",
                "description": (
                    "저장할 데이터 (키: 컬럼명 또는 별칭, 값: 문자열). "
                    "예: {\"expression\": \"pick someone's brain\", "
                    "\"meaning_kr\": \"(조언을) 얻어내다\", "
                    "\"example1\": \"Can I pick your brain?\"}"
                ),
                "additionalProperties": {"type": "string"},
            },
        },
        "required": ["sheet", "data"],
    },
}


def run(client: SheetsClient, sheet: str, data: dict[str, str]) -> str:
    schema = client.registry.get_sheet(sheet)
    row_number, mapped = client.append_row(schema, data)

    lines = [f"✅ '{schema.tab_name}' 시트 {row_number}행에 추가했습니다."]
    for key, value in mapped.items():
        # 길면 자르기
        display = value if len(value) <= 80 else value[:77] + "..."
        lines.append(f"  • {key}: {display}")
    return "\n".join(lines)
