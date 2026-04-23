"""영상 번역 연습을 translation 시트에 저장하는 전용 툴."""
from __future__ import annotations

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "add_translation_row",
    "description": (
        "영상/오디오 번역 연습 결과를 translation 시트에 저장합니다. "
        "사용자가 영상을 보며 번역 연습을 할 때, 원문/내 번역 시도/정답/코멘트를 "
        "한 번에 기록하는 전용 툴입니다."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "original": {
                "type": "string",
                "description": "원문 (영어 또는 대상 언어)",
            },
            "my_try": {
                "type": "string",
                "description": "내가 번역한 결과 (선택)",
            },
            "correct_translation": {
                "type": "string",
                "description": "자연스러운 정답 번역 (선택)",
            },
            "link": {
                "type": "string",
                "description": "영상 URL (선택)",
            },
            "timestamp": {
                "type": "string",
                "description": "영상 타임스탬프 (예: '00:05:30')",
            },
            "comment": {
                "type": "string",
                "description": "차이점·배울 점 코멘트",
            },
            "sheet_alias": {
                "type": "string",
                "description": "저장할 시트 별명. 기본값 'translation'",
                "default": "translation",
            },
        },
        "required": ["original"],
    },
}


def run(
    client: SheetsClient,
    original: str,
    my_try: str = "",
    correct_translation: str = "",
    link: str = "",
    timestamp: str = "",
    comment: str = "",
    sheet_alias: str = "translation",
) -> str:
    schema = client.registry.get_sheet(sheet_alias)
    row_number, _ = client.append_row(
        schema,
        {
            "original": original,
            "my_try": my_try,
            "correct_translation": correct_translation,
            "link": link,
            "timestamp": timestamp,
            "comment": comment,
        },
    )

    lines = [f"✅ '{schema.tab_name}' 시트 {row_number}행에 번역 기록 저장."]
    lines.append(f"  • 원문: {original[:60]}")
    if my_try:
        lines.append(f"  • 내 시도: {my_try[:60]}")
    if correct_translation:
        lines.append(f"  • 자연스러운 번역: {correct_translation[:60]}")
    return "\n".join(lines)
