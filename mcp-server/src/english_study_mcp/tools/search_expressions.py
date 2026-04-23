"""시트에서 표현을 검색하는 툴."""
from __future__ import annotations

import json

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "search_expressions",
    "description": (
        "시트에서 표현을 검색합니다. query가 있으면 모든 컬럼에서 부분일치 검색, "
        "없으면 최근 N개를 반환합니다. 저장 전 중복 체크, 복습 자료 준비, "
        "'어느 시트에 있었더라' 같은 질문에 사용하세요."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "sheet": {
                "type": "string",
                "description": "시트 별명",
            },
            "query": {
                "type": "string",
                "description": "검색어 (선택). 없으면 최근 행 반환.",
            },
            "limit": {
                "type": "integer",
                "description": "최대 반환 개수 (기본 20)",
                "default": 20,
            },
        },
        "required": ["sheet"],
    },
}


def run(
    client: SheetsClient,
    sheet: str,
    query: str | None = None,
    limit: int = 20,
) -> str:
    schema = client.registry.get_sheet(sheet)
    results = client.search(schema, query=query, limit=limit)

    if not results:
        return f"'{schema.tab_name}' 시트에서 결과 없음."

    header = f"'{schema.tab_name}' 시트 - {len(results)}건"
    if query:
        header += f" (검색어: '{query}')"

    return header + "\n" + json.dumps(results, ensure_ascii=False, indent=2)
