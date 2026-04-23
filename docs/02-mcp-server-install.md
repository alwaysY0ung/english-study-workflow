# 02. MCP 서버 설치

## 1. 레포 클론

```bash
git clone https://github.com/<your-username>/english-study-workflow.git
cd english-study-workflow
```

## 2. 가상환경 (권장)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

## 3. 패키지 설치

```bash
cd mcp-server
pip install -e .
```

`mcp`, `gspread`, `google-auth-oauthlib`, `pyyaml` 등이 설치됩니다.

## 4. 최초 OAuth 인증

```bash
python -m english_study_mcp.auth
```

- 브라우저 창이 열립니다
- Google 계정으로 로그인
- "이 앱은 확인되지 않았습니다" 경고가 나와도 **"고급" → "(안전하지 않음)으로 이동"** 으로 진행 (본인이 만든 앱이라 정상)
- Sheets/Drive 권한 허용
- `~/.config/english-study-mcp/token.json`이 생성되면 완료

## 5. 동작 확인

```bash
python -m english_study_mcp.server --check
```

`✅ Google Sheets API 연결 성공` 메시지가 나오면 OK.

## 6. 다음 단계

→ [`03-claude-desktop-config.md`](03-claude-desktop-config.md)

## 트러블슈팅

| 증상 | 해결 |
|---|---|
| `credentials.json not found` | `~/.config/english-study-mcp/credentials.json` 경로 확인 |
| `access_denied` 에러 | OAuth 동의 화면에서 테스트 사용자에 본인 이메일 추가했는지 확인 |
| `invalid_grant` | `token.json` 삭제 후 재인증 |
