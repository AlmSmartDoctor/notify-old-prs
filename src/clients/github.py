from typing import Dict, List, Any
import requests

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_open_prs(self, repo_path: str) -> List[Dict[str, Any]]:
        response = requests.get(
            f"https://api.github.com/repos/{repo_path}/pulls?state=open&per_page=100",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()