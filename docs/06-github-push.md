# 06. GitHub 레포 생성 & 푸시

이 레포를 본인 GitHub 계정으로 올리는 방법.

## 옵션 A: GitHub CLI 사용 (추천)

### 1. GitHub CLI 설치 (한 번만)

**macOS**
```bash
brew install gh
```

**Windows**
```powershell
winget install --id GitHub.cli
```

### 2. 로그인
```bash
gh auth login
```

### 3. 레포 생성 & 푸시 (한 줄)
```bash
cd english-study-workflow
git init
git add .
git commit -m "Initial commit: English study workflow with Claude + Google Sheets MCP"
gh repo create english-study-workflow --public --source=. --push --description "Claude Desktop + Google Sheets MCP로 영어 학습 자동화"
```

완료. 브라우저에서 `https://github.com/<your-username>/english-study-workflow` 확인.

---

## 옵션 B: GitHub 웹 + git push

### 1. GitHub에서 빈 레포 생성
- [github.com/new](https://github.com/new) 접속
- Repository name: `english-study-workflow`
- Public 선택
- **README, .gitignore, license 모두 체크 해제** (이미 있음)
- "Create repository"

### 2. 로컬에서 푸시
```bash
cd english-study-workflow
git init
git add .
git commit -m "Initial commit: English study workflow with Claude + Google Sheets MCP"
git branch -M main
git remote add origin https://github.com/<your-username>/english-study-workflow.git
git push -u origin main
```

---

## 푸시 전 체크리스트 ⚠️

Public 레포이므로 **시크릿이 절대 포함되면 안 됩니다**. 푸시 전 확인:

```bash
# .gitignore가 제대로 적용되는지 확인
git status

# 다음 파일들이 "Untracked files"에 **없어야** 합니다 (있으면 문제):
#   - credentials.json
#   - token.json
#   - config/sheets_registry.yaml  (← .example.yaml만 있어야 함)
#   - .env
```

만약 실수로 커밋했다면:
```bash
git rm --cached credentials.json token.json config/sheets_registry.yaml
git commit -m "Remove accidentally committed secrets"
```

이미 **push까지 했다면** 해당 credential을 Google Cloud에서 즉시 폐기하고 재발급하세요.

---

## 레포 배지 추가 (선택)

README 상단에 아래 배지를 추가하면 보기 좋습니다:

```markdown
![CI](https://github.com/<your-username>/english-study-workflow/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
```

---

## 포크한 사람들을 위한 팁

README에 이미 설정 가이드가 포함되어 있지만, "이 레포를 포크하려면 `<your-username>`을 본인 아이디로 바꿔야 한다"는 안내를 한 줄 추가하면 친절합니다.
