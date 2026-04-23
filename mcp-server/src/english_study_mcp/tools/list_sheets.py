"""등록된 시트 목록과 정보를 반환하는 툴."""
from __future__ import annotations

import json

from ..sheets_client import SheetsClient


TOOL_DEFINITION = {
    "name": "list_sheets",
    "description": (
        "등록된 모든 시트의 별명, 실제 탭 이름, 컬럼 구조, 현재 행 수를 반환합니다. "
        "사용자가 '시트 뭐뭐 있어?' 라고 물을 때 사용하세요."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {},
    },
}


def run(client: SheetsClient) -> str:
    infos = []
    for alias in client.registry.sheets:
        schema = client.registry.get_sheet(alias)
        try:
            infos.append(client.sheet_info(schema))
        except Exception as e:  # 탭이 없거나 접근 불가
            infos.append({
                "alias": alias,
                "tab_name": schema.tab_name,
                "error": str(e),
            })

    return json.dumps(infos, ensure_ascii=False, indent=2)
