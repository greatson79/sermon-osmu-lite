#!/usr/bin/env python3
"""Optional, explicit upload to a user owned YouTube channel."""
import argparse
import pathlib


def main():
    parser = argparse.ArgumentParser(description="Upload a reviewed video to your own channel")
    parser.add_argument("--file", type=pathlib.Path, required=True)
    parser.add_argument("--client-json", type=pathlib.Path, required=True)
    parser.add_argument("--token-json", type=pathlib.Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--tags", default="")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--confirm-upload", action="store_true", help="Required to perform an upload")
    args = parser.parse_args()
    if not args.confirm_upload:
        parser.error("upload disabled; pass --confirm-upload after review and authorization")
    if not args.file.is_file() or not args.client_json.is_file():
        print("텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: 완성 영상 + 유튜브 OAuth 클라이언트 JSON)")
        return
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: pip install google-api-python-client google-auth-oauthlib)")
        return

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = Credentials.from_authorized_user_file(str(args.token_json), scopes) if args.token_json.is_file() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(args.client_json), scopes)
            creds = flow.run_local_server(port=0)
        args.token_json.parent.mkdir(parents=True, exist_ok=True)
        args.token_json.write_text(creds.to_json(), encoding="utf-8")
        args.token_json.chmod(0o600)
    snippet = {"title": args.title, "description": args.description, "categoryId": "22"}
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    if tags:
        snippet["tags"] = tags
    body = {"snippet": snippet, "status": {"privacyStatus": args.privacy}}
    service = build("youtube", "v3", credentials=creds)
    request = service.videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload(str(args.file), resumable=True))
    response = None
    while response is None:
        _, response = request.next_chunk()
    print(f"uploaded video id: {response['id']}")


if __name__ == "__main__":
    main()
