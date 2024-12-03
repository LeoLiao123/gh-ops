import os
import yaml

def load_config() -> str:
    if os.path.exists('config.yaml'):
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f).get('github_token')
    return os.getenv('GITHUB_TOKEN')
