import re
import requests
import argparse
from typing import Tuple, Dict, List

class GitHubPRDiffFetcher:
    def __init__(self, github_token: str):
        """
        Initialize GitHub API client
        
        Args:
            github_token (str): GitHub personal access token
        """
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'

    def parse_pr_url(self, pr_url: str) -> Tuple[str, str, str]:
        """
        Parse GitHub PR URL to extract owner, repo and PR number
        
        Args:
            pr_url (str): PR URL in format https://github.com/owner/repo/pull/number
            
        Returns:
            Tuple[str, str, str]: (owner, repo, pr_number)
        """
        pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.search(pattern, pr_url)
        if not match:
            raise ValueError("Invalid GitHub PR URL format")
        return match.group(1), match.group(2), match.group(3)

    def get_pr_changes(self, pr_url: str) -> List[Dict]:
        """
        Get detailed changes for each file in the PR
        
        Args:
            pr_url (str): PR URL
            
        Returns:
            List[Dict]: List of file changes with detailed patch information
        """
        owner, repo, pr_number = self.parse_pr_url(pr_url)
        
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()

    def extract_code_changes(self, patch: str) -> Tuple[List[str], List[str]]:
        """
        Extract added and deleted lines from a patch
        
        Args:
            patch (str): Git patch content
            
        Returns:
            Tuple[List[str], List[str]]: Lists of added and deleted lines
        """
        added_lines = []
        deleted_lines = []
        
        if not patch:
            return added_lines, deleted_lines
            
        for line in patch.split('\n'):
            # Skip diff metadata lines
            if line.startswith(('@@', 'diff', 'index', '---', '+++')):
                continue
                
            # Extract actual code changes
            if line.startswith('+') and not line.startswith('+++'):
                added_lines.append(line[1:])
            elif line.startswith('-') and not line.startswith('---'):
                deleted_lines.append(line[1:])
                
        return added_lines, deleted_lines

def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Fetch GitHub PR diff information')
    parser.add_argument('url', help='GitHub PR URL')
    parser.add_argument('--token', '-t', 
                      help='GitHub personal access token. If not provided, will try to read from GITHUB_TOKEN environment variable',
                      default=None)
    
    args = parser.parse_args()
    
    # Get GitHub token from args or environment variable
    token = args.token
    if not token:
        import os
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            print("Error: GitHub token not provided. Please either:")
            print("1. Use --token or -t option")
            print("2. Set GITHUB_TOKEN environment variable")
            return
    
    try:
        fetcher = GitHubPRDiffFetcher(token)
        
        # Get file changes
        changes = fetcher.get_pr_changes(args.url)
        total_additions = 0
        total_deletions = 0
        
        # Process each changed file
        for file_change in changes:
            filename = file_change['filename']
            additions = file_change['additions']
            deletions = file_change['deletions']
            patch = file_change.get('patch', '')
            
            total_additions += additions
            total_deletions += deletions
            
            # Extract and display code changes
            added_lines, deleted_lines = fetcher.extract_code_changes(patch)
            
            print(f"\n\n{'-'*80}")
            print(f"File: {filename}")
            print(f"Changes: +{additions} -{deletions}")
            print('-'*80)
            
            if deleted_lines:
                print("\nDeleted lines:")
                print('-'*40)
                for line in deleted_lines:
                    print(f"\033[91m- {line}\033[0m")  # Red color for deletions
            
            if added_lines:
                print("\nAdded lines:")
                print('-'*40)
                for line in added_lines:
                    print(f"\033[92m+ {line}\033[0m")  # Green color for additions
        
        print(f"\n{'-'*80}")
        print(f"Total changes: +{total_additions} -{total_deletions}")
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {str(e)}")
        if e.response.status_code == 401:
            print("Authentication failed. Please check your GitHub token.")
        elif e.response.status_code == 404:
            print("PR not found. Please check the URL.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()