import os
import subprocess
import requests

# Replace 'USERNAME' with the target GitHub username
GITHUB_USERNAME = "aidenwong812"
CLONE_DIRECTORY = "./github_repos"  # Directory where repos will be cloned

def get_public_repos(username):
    """
    Fetch the list of public repositories for a given GitHub username.
    """
    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch repos: {response.status_code}")
            break

        data = response.json()
        if not data:
            break  # No more repositories to fetch

        repos.extend([repo['clone_url'] for repo in data])
        page += 1

    return repos

def clone_repositories(repo_urls, target_directory):
    """
    Clone repositories from the list of URLs into the specified directory.
    """
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for repo_url in repo_urls:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(target_directory, repo_name)
        
        if os.path.exists(target_path):
            print(f"Skipping '{repo_name}', already exists.")
            continue

        print(f"Cloning {repo_url} into {target_path}...")
        try:
            subprocess.run(["git", "clone", repo_url, target_path], check=True)
            print(f"Successfully cloned {repo_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning {repo_name}: {e}")

def main():
    githubusers = [
                # "guman24",
                # "Montedev0516",
                # "futuresea-dev",
                # "Uhmopt",
                # "Devflames",
                # "Farhan-12",
                # "better-think"
                "james-mensa"
                ]

    for username in githubusers : 
        print(f"Fetching repositories for user '{username}'...")
        repo_urls = get_public_repos(username)

        if not repo_urls:
            print("No repositories found or failed to fetch.")
            continue

        print(f"Found {len(repo_urls)} repositories.")
        clone_repositories(repo_urls, CLONE_DIRECTORY)
        print("All repositories have been cloned.")

if __name__ == "__main__":
    main()