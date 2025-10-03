import requests
from fastapi import HTTPException
from cfg.settings import GITHUB_BASE_URL
from creds.storage import load_credentials

class GitHubClient:
    def __init__(self, owner: str, repo: str, token: str = None):
        self.owner = owner
        self.repo = repo
        self.token = token

    def _headers(self):
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(self, method: str, path: str, json_body=None):
        url = f"{GITHUB_BASE_URL}{path}"
        r = requests.request(method, url, headers=self._headers(), json=json_body)
        if not r.ok:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        try:
            return r.json()
        except ValueError:
            return r.text

    # CRUD
    def list_releases(self):
        return self._request("GET", f"/repos/{self.owner}/{self.repo}/releases")

    def get_release(self, release_id: int):
        return self._request("GET", f"/repos/{self.owner}/{self.repo}/releases/{release_id}")

    def create_release(self, tag_name: str, name: str, body: str = ""):
        return self._request("POST", f"/repos/{self.owner}/{self.repo}/releases",
                             {"tag_name": tag_name, "name": name, "body": body})

    def update_release(self, release_id: int, name: str = None, body: str = None):
        payload = {}
        if name: payload["name"] = name
        if body: payload["body"] = body
        return self._request("PATCH", f"/repos/{self.owner}/{self.repo}/releases/{release_id}", payload)

    def delete_release(self, release_id: int):
        return self._request("DELETE", f"/repos/{self.owner}/{self.repo}/releases/{release_id}")

# Загрузка кредов 1 раз при старте
creds = load_credentials()
github_client = GitHubClient(creds["owner"], creds["repo"], creds.get("token"))
