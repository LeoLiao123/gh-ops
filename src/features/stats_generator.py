from ..core.github_client import GitHubClient
from collections import Counter

class StatsGenerator:
    def __init__(self, token: str):
        self.client = GitHubClient(token)

    def process(self, pr_url: str):
        owner, repo, pr_number = self.client.parse_pr_url(pr_url)
        files = self.client.get_pr_files(owner, repo, pr_number)
        reviews = self.client.get_pr_reviews(owner, repo, pr_number)
        
        extensions = Counter(
            f.split('.')[-1] for f in [f['filename'] for f in files] 
            if '.' in f
        )
        
        print("\nPR Statistics:")
        print(f"Total files changed: {len(files)}")
        print("\nFile types:")
        for ext, count in extensions.most_common():
            print(f"- .{ext}: {count} files")
        print(f"\nTotal reviews: {len(reviews)}")
