import os
import requests
from github import Github

# Configuration
token = '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'  # Replace with your GitHub token
search_query = 'taipy in:name'  # Search for repos with 'taipy' in their name
destination_folder = 'taipy_repos'  # Folder to store the repositories

# Initialize GitHub
g = Github(token)

# Search for repositories
repos = g.search_repositories('taipy in:name')

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Clone each repository
for repo in repos:
    clone_url = repo.clone_url
    os.system(f'git clone {clone_url} {destination_folder}/{repo.name}')

print(f"All repositories named '{search_query}' have been cloned into '{destination_folder}'")
