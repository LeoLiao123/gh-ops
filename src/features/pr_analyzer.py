from ..github_client import GitHubClient

class PRAnalyzer:
    def __init__(self, token: str):
        self.client = GitHubClient(token)

    def format_diff(self, file_change: dict):
        filename = file_change['filename']
        additions = file_change['additions']
        deletions = file_change['deletions']
        patch = file_change.get('patch', '')
        
        print(f"\n{'='*80}")
        print(f"File: {filename}")
        print(f"Changes: +{additions} -{deletions}")
        print('='*80)
        
        if not patch:
            return
            
        for line in patch.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                print(f"\033[92m{line}\033[0m")
            elif line.startswith('-') and not line.startswith('---'):
                print(f"\033[91m{line}\033[0m")
            else:
                print(line)

    def process(self, pr_url: str):
        owner, repo, pr_number = self.client.parse_pr_url(pr_url)
        changes = self.client.get_pr_files(owner, repo, pr_number)
        
        total_additions = sum(change['additions'] for change in changes)
        total_deletions = sum(change['deletions'] for change in changes)
        
        for file_change in changes:
            self.format_diff(file_change)
            
        print(f"\nTotal: +{total_additions} -{total_deletions}")
