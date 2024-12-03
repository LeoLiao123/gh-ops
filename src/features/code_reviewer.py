from ..github_client import GitHubClient
import re

class CodeReviewer:
    def __init__(self, token: str):
        self.client = GitHubClient(token)
        
    def check_code_quality(self, content: str) -> list:
        issues = []
        
        if len(content.split('\n')) > 300:
            issues.append("File too long (>300 lines)")
        if re.search(r'print\(', content):
            issues.append("Contains print statements")
        if re.search(r'TODO|FIXME', content):
            issues.append("Contains TODO/FIXME comments")
        
        return issues

    def process(self, pr_url: str):
        owner, repo, pr_number = self.client.parse_pr_url(pr_url)
        files = self.client.get_pr_files(owner, repo, pr_number)
        
        for file in files:
            if file['filename'].endswith(('.py', '.js', '.java')):
                print(f"\nAnalyzing {file['filename']}:")
                issues = self.check_code_quality(file.get('patch', ''))
                for issue in issues:
                    print(f"- {issue}")
