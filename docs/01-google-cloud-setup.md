# 01. Google Cloud 설정

Google Sheets API를 사용하려면 OAuth 2.0 클라이언트를 발급받아야 합니다. **모두 무료 티어 안에서 이뤄지며, 신용카드 등록이 필요 없습니다.**

## 1. 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 상단 프로젝트 드롭다운 → "새 프로젝트"
3. 이름 예: `english-study-mcp`

## 2. API 활성화

"API 및 서비스" → "라이브러리"에서 다음 두 개를 검색해 **각각 사용 설정** 클릭:

- **Google Sheets API**
- **Google Drive API** (시트 목록/검색에 필요)

## 3. OAuth 동의 화면

"API 및 서비스" → "OAuth 동의 화면":

1. User Type: **외부(External)**
2. 앱 이름: 예 `English Study MCP`
3. 사용자 지원 이메일 / 개발자 연락처: 본인 이메일
4. 범위(Scopes): 기본값 유지 후 저장
5. **테스트 사용자**에 본인 Google 계정 이메일 추가 — 중요!

> 앱을 "게시"할 필요 없음. 테스트 사용자 상태로 영구 사용 가능.

## 4. OAuth 클라이언트 ID 발급

"API 및 서비스" → "사용자 인증 정보" → "사용자 인증 정보 만들기" → **OAuth 클라이언트 ID**:

1. 애플리케이션 유형: **데스크톱 앱**
2. 이름: 예 `english-study-desktop`
3. 만들기 → **JSON 다운로드**

## 5. credentials.json 배치

다운로드한 JSON을 아래 경로로 이동:

```bash
mkdir -p ~/.config/english-study-mcp
mv ~/Downloads/client_secret_*.json ~/.config/english-study-mcp/credentials.json
```

## 6. 다음 단계

→ [`02-mcp-server-install.md`](02-mcp-server-install.md)
