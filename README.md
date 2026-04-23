# English Study Workflow

Claude Desktop + Google Sheets를 연결해 영어 표현 학습을 자동화하는 개인 워크플로우.

질문만 하면 Claude가 의미·뉘앙스·예문을 설명하고, **"정리해줘" 한 마디로** 적절한 Google Sheets에 자동 저장됩니다.

![CI](https://github.com/<your-username>/english-study-workflow/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

> ✨ Claude 구독료 외 **추가 비용 0원**. 모든 것은 로컬에서 실행되고 Google API 무료 할당량 내에서 동작합니다.

---

## 🧩 아키텍처

```
 ┌──────────────────┐        ┌───────────────────────┐       ┌──────────────────┐
 │  Claude Desktop  │ ◀────▶ │  english-study-mcp    │ ◀───▶ │  Google Sheets   │
 │  (채팅 UI)        │  MCP   │  (로컬 Python 서버)     │ OAuth │  (5개 학습 시트)   │
 └──────────────────┘        └───────────────────────┘       └──────────────────┘
         ▲                          │
         │  Project Instructions    │  8 tools:
         │  + Sheet registry        │  add/search/list/quiz/
         │                          │  correct/translate/update/review
```

---

## 📋 5개 활성 시트

| 시트 | 용도 |
|---|---|
| **daily** | 일반 영어 표현·단어·구동사·숙어 학습 |
| **corrections** | 내 영어 문장 → 자연스러운 교정 + 발음 팁 |
| **pronunciation** | 발음·억양 전용 팁 |
| **assertions** | 시험 대비 Unit별 주장 + 근거 |
| **translation** | 영상/오디오 번역 연습 (원문 vs 내 시도 vs 정답) |

## 🛠 8개 MCP 툴

**기본 툴 (4개)**
- `add_expression` — 표현을 시트에 추가 (컬럼 자동 매핑)
- `search_expressions` — 검색, 중복 체크
- `list_sheets` — 시트 목록·구조 조회
- `quiz_random` — 복습 퀴즈용 랜덤 샘플

**특화 툴 (4개)**
- `correct_expression` — corrections 시트 전용 (my_version/corrected/reason 한번에)
- `add_translation_row` — translation 시트 전용 (영상 번역 연습)
- `update_expression` — 기존 행 수정·예문 추가
- `weekly_review` — 기간별 학습 데이터 집계 (Claude가 분석 제공)

---

## 🚀 빠른 시작

### 요구사항
- Python 3.10+
- Claude Desktop ([다운로드](https://claude.ai/download))
- Google 계정

### 1. 설치
```bash
git clone https://github.com/<your-username>/english-study-workflow.git
cd english-study-workflow

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

cd mcp-server
pip install -e .
```

### 2. Google Cloud 설정
자세한 가이드: [`docs/01-google-cloud-setup.md`](docs/01-google-cloud-setup.md)

요약:
1. Google Cloud Console에서 새 프로젝트 생성
2. Sheets API + Drive API 활성화
3. OAuth 2.0 클라이언트 ID (데스크톱 앱) 발급 → `credentials.json`
4. `~/.config/english-study-mcp/credentials.json` 으로 이동

### 3. 최초 인증
```bash
python -m english_study_mcp.auth
```
브라우저가 열리면 Google 로그인 → "고급" → "(안전하지 않음)으로 이동" → 권한 허용. `token.json`이 자동 저장됨.

### 4. Google Sheets 준비
재구성된 엑셀 파일을 Google Drive에 업로드 → Google Sheets로 변환.  
또는 빈 시트에 직접 5개 탭 생성. 상세: [`docs/04-sheet-schema.md`](docs/04-sheet-schema.md)

### 5. 시트 레지스트리 설정
```bash
cp config/sheets_registry.example.yaml config/sheets_registry.yaml
```
`spreadsheet_id`에 본인 Sheets ID 입력.

### 6. Claude Desktop 연결
`config/claude_desktop_config.example.json` 참고해 Claude Desktop 설정에 MCP 서버 추가:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

상세: [`docs/03-claude-desktop-config.md`](docs/03-claude-desktop-config.md)

### 7. Project 생성
Claude Desktop에서 새 Project → Instructions에 [`prompts/project-instructions.md`](prompts/project-instructions.md) 붙여넣기.

---

## 💬 사용 예시

```
나: "pick someone's brain 이 표현 뭐야?"

Claude: [의미·뉘앙스·예문 3개 설명]

나: "daily에 정리해줘"

Claude: [search_expressions로 중복 체크 → add_expression]
✅ daily 시트 111행에 추가했어요.
```

더 많은 예시: [`docs/05-usage-examples.md`](docs/05-usage-examples.md) — 5개 시트 × 8개 툴 조합 시나리오 포함.

---

## 📂 레포 구조

```
english-study-workflow/
├── README.md, LICENSE, .gitignore
├── docs/                           # 1~6번 세팅 & 사용 가이드
├── prompts/                        # Project Instructions, 프롬프트 템플릿
├── config/                         # *.example.* (본인 값은 로컬에만)
└── mcp-server/                     # 커스텀 MCP 서버
    ├── pyproject.toml
    └── src/english_study_mcp/
        ├── server.py               # 엔트리포인트, 8개 툴 등록
        ├── auth.py                 # OAuth 최초 인증
        ├── sheets_client.py        # gspread 래퍼
        ├── schemas/registry.py     # YAML 스키마 로더
        └── tools/                  # 8개 툴 구현
            ├── add_expression.py
            ├── search_expressions.py
            ├── list_sheets.py
            ├── quiz_random.py
            ├── correct_expression.py
            ├── add_translation_row.py
            ├── update_expression.py
            └── weekly_review.py
```

---

## 🔐 시크릿 관리 (Public repo 주의사항)

`.gitignore`에 다음이 포함되어 있어 푸시되지 않습니다:
- `credentials.json` / `token.json` — OAuth 시크릿
- `config/sheets_registry.yaml` — 본인 시트 ID
- `.env`

본인 설정 파일은 `~/.config/english-study-mcp/` 아래나 로컬에만 두세요.

---

## 🛠 커스터마이즈

- **새 툴 추가**: `mcp-server/src/english_study_mcp/tools/`에 파일 추가 후 `server.py`에 등록
- **시트 스키마 변경**: `config/sheets_registry.yaml` 수정 (코드 수정 불필요)
- **프롬프트 조정**: `prompts/project-instructions.md`

---

## 📜 라이선스

MIT License. 포크해서 자유롭게 사용하세요.

## 🙏 Acknowledgments

- [Anthropic Claude](https://www.anthropic.com/) + [Model Context Protocol](https://modelcontextprotocol.io/)
- [gspread](https://github.com/burnash/gspread) — Google Sheets Python 라이브러리
