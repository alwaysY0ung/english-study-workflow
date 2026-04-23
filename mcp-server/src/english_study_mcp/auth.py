"""OAuth 최초 인증 스크립트.

사용법:
    python -m english_study_mcp.auth
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

CONFIG_DIR = Path(
    os.environ.get("ENGLISH_STUDY_CONFIG_DIR", Path.home() / ".config" / "english-study-mcp")
)
CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"
TOKEN_PATH = CONFIG_DIR / "token.json"


def get_credentials() -> Credentials:
    """저장된 토큰을 불러오거나, 없으면 최초 OAuth 플로우 실행."""
    creds: Credentials | None = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    f"credentials.json이 없습니다: {CREDENTIALS_PATH}\n"
                    f"docs/01-google-cloud-setup.md 를 참고해 OAuth 클라이언트를 발급받으세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())

    return creds


def main() -> int:
    try:
        creds = get_credentials()
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    if creds.valid:
        print("✅ OAuth 인증 완료")
        print(f"   토큰 저장 위치: {TOKEN_PATH}")
        return 0
    print("❌ 인증 실패", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
