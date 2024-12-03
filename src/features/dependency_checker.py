from ..core.github_client import GitHubClient
import yaml

class DependencyChecker:
    def __init__(self, token: str):
        self.client = GitHubClient(token)

    def check_dependencies(self, content: str) -> list:
        try:
            deps = yaml.safe_load(content)
            return [(name, version) 
                    for name, version in deps.get('dependencies', {}).items()]
        except:
            return []

    def process(self, pr_url: str):
        owner, repo, pr_number = self.client.parse_pr_url(pr_url)
        files = self.client.get_pr_files(owner, repo, pr_number)
        
        for file in files:
            if file['filename'] in ['requirements.txt', 'package.json', 'pom.xml']:
                print(f"\nChecking dependencies in {file['filename']}:")
                deps = self.check_dependencies(file.get('patch', ''))
                for name, version in deps:
                    print(f"- {name}: {version}")
