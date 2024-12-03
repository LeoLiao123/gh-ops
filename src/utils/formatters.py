def format_diff(file_change: dict):
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