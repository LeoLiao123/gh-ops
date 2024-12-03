import re
import requests
from typing import Tuple, Dict, List

class GitHubClient:
    def __init__(self, token: str):
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'

    def parse_pr_url(self, pr_url: str) -> Tuple[str, str, str]:
        pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.search(pattern, pr_url)
        if not match:
            raise ValueError("Invalid GitHub PR URL")
        return match.group(1), match.group(2), match.group(3)

    def get_pr_files(self, owner: str, repo: str, pr_number: str) -> List[Dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_pr_reviews(self, owner: str, repo: str, pr_number: str) -> List[Dict]:
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()