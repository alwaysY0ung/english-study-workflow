"""MCP 서버 엔트리포인트.

실행:
    python -m english_study_mcp.server           # Claude Desktop에서 호출됨
    python -m english_study_mcp.server --check   # 연결 체크만
"""
from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .schemas.registry import load_registry
from .sheets_client import SheetsClient
from .tools import (
    add_expression,
    add_translation_row,
    correct_expression,
    list_sheets,
    quiz_random,
    search_expressions,
    update_expression,
    weekly_review,
)

logger = logging.getLogger("english-study-mcp")

# 툴 이름 → (정의, 실행 함수)
TOOLS = {
    add_expression.TOOL_DEFINITION["name"]: (
        add_expression.TOOL_DEFINITION,
        add_expression.run,
    ),
    search_expressions.TOOL_DEFINITION["name"]: (
        search_expressions.TOOL_DEFINITION,
        search_expressions.run,
    ),
    list_sheets.TOOL_DEFINITION["name"]: (
        list_sheets.TOOL_DEFINITION,
        list_sheets.run,
    ),
    quiz_random.TOOL_DEFINITION["name"]: (
        quiz_random.TOOL_DEFINITION,
        quiz_random.run,
    ),
    correct_expression.TOOL_DEFINITION["name"]: (
        correct_expression.TOOL_DEFINITION,
        correct_expression.run,
    ),
    add_translation_row.TOOL_DEFINITION["name"]: (
        add_translation_row.TOOL_DEFINITION,
        add_translation_row.run,
    ),
    update_expression.TOOL_DEFINITION["name"]: (
        update_expression.TOOL_DEFINITION,
        update_expression.run,
    ),
    weekly_review.TOOL_DEFINITION["name"]: (
        weekly_review.TOOL_DEFINITION,
        weekly_review.run,
    ),
}


def build_server() -> tuple[Server, SheetsClient]:
    registry = load_registry()
    client = SheetsClient(registry)
    server: Server = Server("english-study")

    @server.list_tools()
    async def list_tools_handler() -> list[Tool]:
        return [
            Tool(
                name=defn["name"],
                description=defn["description"],
                inputSchema=defn["inputSchema"],
            )
            for defn, _ in TOOLS.values()
        ]

    @server.call_tool()
    async def call_tool_handler(
        name: str, arguments: dict[str, Any] | None
    ) -> list[TextContent]:
        if name not in TOOLS:
            return [TextContent(type="text", text=f"❌ 알 수 없는 툴: {name}")]

        _, run_fn = TOOLS[name]
        args = arguments or {}

        try:
            # list_sheets는 인자 없음
            if name == "list_sheets":
                result = run_fn(client)
            else:
                result = run_fn(client, **args)
        except Exception as e:
            logger.exception("툴 실행 실패: %s", name)
            return [TextContent(type="text", text=f"❌ 에러: {e}")]

        return [TextContent(type="text", text=result)]

    return server, client


async def _run_server() -> None:
    server, _ = build_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def check_connection() -> int:
    """연결 상태만 점검하고 종료."""
    try:
        _, client = build_server()
        info = [client.sheet_info(client.registry.get_sheet(a)) for a in client.registry.sheets]
        print("✅ Google Sheets API 연결 성공")
        print(f"   spreadsheet_id: {client.registry.spreadsheet_id}")
        print(f"   등록된 시트 {len(info)}개:")
        for i in info:
            print(f"     - {i['alias']} ({i['tab_name']}): {i.get('row_count', '?')}행")
        return 0
    except Exception as e:
        print(f"❌ 연결 실패: {e}", file=sys.stderr)
        return 1


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    if "--check" in sys.argv:
        return check_connection()

    asyncio.run(_run_server())
    return 0


if __name__ == "__main__":
    sys.exit(main())
