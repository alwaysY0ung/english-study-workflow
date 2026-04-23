"""내 영어 → 교정을 corrections 시트에 저장하는 전용 툴."""
from __future__ import annotations

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "correct_expression",
    "description": (
        "내 영어 표현·문장을 교정한 내용을 corrections 시트에 저장합니다. "
        "사용자가 '이 문장 자연스러워?' / '이거 교정해줘' 라고 물어본 뒤, "
        "저장을 요청할 때 사용하세요. corrections 시트의 특수 구조에 맞춰 "
        "my_version, corrected, reason, pronunciation_tip을 한 번에 기록합니다. "
        "sheet_alias는 기본 'corrections'이지만 다른 시트에서도 동일 구조가 있다면 지정 가능합니다."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "my_version": {
                "type": "string",
                "description": "내가 원래 말하거나 쓴 영어 표현",
            },
            "corrected": {
                "type": "string",
                "description": "자연스럽게 교정된 표현",
            },
            "reason": {
                "type": "string",
                "description": "교정한 이유, 문법 설명, 어휘 선택 근거 등",
            },
            "pronunciation_tip": {
                "type": "string",
                "description": "발음·억양 팁 (선택)",
            },
            "topic": {
                "type": "string",
                "description": "주제·카테고리 (선택, 예: '논문 작성', '면접')",
            },
            "sheet_alias": {
                "type": "string",
                "description": "저장할 시트 별명. 기본값 'corrections'",
                "default": "corrections",
            },
        },
        "required": ["my_version", "corrected"],
    },
}


def run(
    client: SheetsClient,
    my_version: str,
    corrected: str,
    reason: str = "",
    pronunciation_tip: str = "",
    topic: str = "",
    sheet_alias: str = "corrections",
) -> str:
    schema = client.registry.get_sheet(sheet_alias)
    row_number, mapped = client.append_row(
        schema,
        {
            "my_version": my_version,
            "corrected": corrected,
            "reason": reason,
            "pronunciation_tip": pronunciation_tip,
            "topic": topic,
        },
    )

    lines = [f"✅ '{schema.tab_name}' 시트 {row_number}행에 교정 저장."]
    lines.append(f"  • Before: {my_version}")
    lines.append(f"  • After:  {corrected}")
    if reason:
        lines.append(f"  • 이유: {reason[:80]}")
    return "\n".join(lines)
