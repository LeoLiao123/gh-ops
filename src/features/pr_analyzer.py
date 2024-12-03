from ..core.github_client import GitHubClient
from ..utils.formatters import format_diff

class PRAnalyzer:
    def __init__(self, token: str):
        self.client = GitHubClient(token)

    def process(self, pr_url: str):
        owner, repo, pr_number = self.client.parse_pr_url(pr_url)
        changes = self.client.get_pr_files(owner, repo, pr_number)
        
        total_additions = sum(change['additions'] for change in changes)
        total_deletions = sum(change['deletions'] for change in changes)
        
        for file_change in changes:
            format_diff(file_change)
            
        print(f"\nTotal: +{total_additions} -{total_deletions}")
