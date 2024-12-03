from ..utils.config import load_config
from ..features import PRAnalyzer, CodeReviewer, DependencyChecker, StatsGenerator
from ..utils.constants import FEATURES

class GitHubAssistant:
    def __init__(self):
        self.token = load_config()
        self.features = FEATURES

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
