# 03. Claude Desktop 연결

## 1. 설정 파일 열기

**macOS**
```bash
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**
```
notepad %APPDATA%\Claude\claude_desktop_config.json
```

파일이 없으면 새로 만드세요.

## 2. MCP 서버 등록

`config/claude_desktop_config.example.json`을 참고해 다음을 추가:

```json
{
  "mcpServers": {
    "english-study": {
      "command": "<YOUR_HOME>/miniforge3/envs/english-study-mcp/bin/python",
      "args": ["-m", "english_study_mcp.server"],
      "env": {
        "ENGLISH_STUDY_CONFIG": "<ABSOLUTE_PATH_TO_REPO>/config/sheets_registry.yaml"
      }
    }
  }
}
```

### 경로 팁

- **Python 경로**: mamba 환경의 python 절대경로 사용
  - 확인: `mamba activate english-study-mcp && which python`
  - 기본 위치: `<YOUR_HOME>/miniforge3/envs/english-study-mcp/bin/python`
- **설정 파일 경로**: `sheets_registry.yaml` 절대 경로

이미 다른 MCP 서버가 등록되어 있다면 `mcpServers` 객체 안에 `english-study` 항목만 추가.

## 3. Claude Desktop 재시작

완전히 종료 후 재실행 (macOS는 ⌘Q).

## 4. 동작 확인

Claude Desktop 하단의 🔌 아이콘 클릭 → `english-study` 서버가 연결되어 있고 툴 목록이 보이면 성공:

- `add_expression`
- `search_expressions`
- `list_sheets`
- `quiz_random`
- `correct_expression`
- `add_translation_row`
- `update_expression`
- `weekly_review`

## 5. 다음 단계

→ [`04-sheet-schema.md`](04-sheet-schema.md)

## 트러블슈팅

| 증상 | 해결 |
|---|---|
| 🔌 아이콘에 서버가 안 보임 | `claude_desktop_config.json` 문법 오류 확인 (JSON validator 사용) |
| `command not found` | Python 경로를 절대경로로 변경, `mamba env list`로 환경 존재 확인 |
| 서버 연결은 되나 툴 호출 시 에러 | `token.json` 존재 확인, 재인증 시도 |
