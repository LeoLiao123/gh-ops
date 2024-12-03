import os
import yaml
from src.features import PRAnalyzer, CodeReviewer, DependencyChecker, StatsGenerator

class GitHubAssistant:
    def __init__(self):
        self.token = self.load_config()
        self.features = {
            '1': ('Analyze PR Changes', PRAnalyzer),
            '2': ('Review Code Quality', CodeReviewer),
            '3': ('Check Dependencies', DependencyChecker),
            '4': ('Generate PR Statistics', StatsGenerator),
            '5': ('Exit', None)
        }

    def load_config(self):
        if os.path.exists('config.yaml'):
            with open('config.yaml', 'r') as f:
                return yaml.safe_load(f).get('github_token')
        return os.getenv('GITHUB_TOKEN')

    def display_menu(self):
        print("\nGitHub PR Assistant")
        print("-" * 20)
        for key, (name, _) in self.features.items():
            print(f"{key}. {name}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nSelect an option: ")
            
            if choice == '5':
                print("Goodbye!")
                break
                
            if choice not in self.features:
                print("Invalid option.")
                continue

            _, feature_class = self.features[choice]
            pr_url = input("Enter PR URL: ")
            
            try:
                feature = feature_class(self.token)
                feature.process(pr_url)
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    GitHubAssistant().run()