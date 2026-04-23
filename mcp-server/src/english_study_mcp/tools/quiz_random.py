"""랜덤 퀴즈 샘플을 반환하는 툴."""
from __future__ import annotations

import json

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "quiz_random",
    "description": (
        "복습 퀴즈용으로 시트에서 랜덤 샘플을 추출합니다. "
        "사용자가 '퀴즈 내줘', '복습하자' 라고 할 때 사용하세요. "
        "Claude는 반환된 데이터로 직접 퀴즈 형식을 구성하세요 "
        "(예: 한국어 뜻만 보여주고 영어 표현 맞추기)."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "sheet": {
                "type": "string",
                "description": "시트 별명",
            },
            "count": {
                "type": "integer",
                "description": "샘플 개수 (기본 5)",
                "default": 5,
            },
        },
        "required": ["sheet"],
    },
}


def run(client: SheetsClient, sheet: str, count: int = 5) -> str:
    schema = client.registry.get_sheet(sheet)
    samples = client.random_sample(schema, count=count)

    if not samples:
        return f"'{schema.tab_name}' 시트가 비어있음."

    return json.dumps(samples, ensure_ascii=False, indent=2)
