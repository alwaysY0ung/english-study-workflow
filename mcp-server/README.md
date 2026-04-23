# english-study-mcp

영어 공부 워크플로우용 MCP 서버. Google Sheets에 표현을 체계적으로 저장·조회합니다.

## 제공 툴

| 툴 | 설명 |
|---|---|
| `list_sheets` | 등록된 시트 목록과 각 시트 정보 |
| `add_expression` | 시트에 새 표현 추가 (컬럼 자동 매핑) |
| `search_expressions` | 시트에서 표현 검색 (중복 체크, 필터) |
| `quiz_random` | 랜덤 샘플 반환 (복습 퀴즈용) |

## 개발

```bash
cd mcp-server
pip install -e ".[dev]"
pytest
```

## 아키텍처

```
server.py          ← MCP 프로토콜 엔트리포인트
├── sheets_client  ← gspread 래퍼
├── schemas/       ← YAML 로드, 컬럼 매핑
└── tools/         ← 각 MCP 툴 구현
```

자세한 설정은 상위 레포의 [`docs/`](../docs/) 참고.
