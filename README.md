# GithubOps
A personal command-line utility leveraging the GitHub API to streamline pull request management and code review workflows.
## Features
* Pull Request Analysis: Extract and visualize code changes with syntax highlighting
* Code Quality Review: Automated checks for code style and potential issues
* Dependency Analysis: Track and analyze project dependencies
* PR Statistics: Generate comprehensive metrics and insights
## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/github-pr-assistant.git

# Create virtual environment
python -m venv env
source env/bin/activate  # For Unix
# or
.\env\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

```
## Configuration
Create a `config.yaml` file in the root directory:
```yaml
yamlCopygithub_token: "your-github-token"

```
## Usage
```bash
Copypython main.py
```
