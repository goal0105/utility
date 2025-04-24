import requests
import json
import os
from subprocess import call, Popen, PIPE
from git import Repo

GITHUB_USERS = [
    # "guman24",
    "montedev0516",
    # "futuresea-dev",
    # "Uhmopt",
    # "Devflames",
    # "Farhan-12",
    # "better-think"
    "james-mensa"
    ]

# GitHub Personal Access Token and Username
GITHUB_TOKEN = "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"
g_name = "goal0105"
g_email = "ronipeterstar@gmail.com"

def test_github_token():
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Authentication successful!")
        print(response.json())
    else:
        print(f"Failed to authenticate: {response.status_code}")
        print(response.json())

def create_github_new_repo(token, username, repo_name):

    print("Creating repository")
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "name": repo_name,
        "private": True,
        "description": "This repository was created via Python automation."
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"GitHub repository '{repo_name}' created successfully.")
        return response.json()["clone_url"]
    elif response.status_code == 422:
        print(f"Repository '{repo_name}' already exists on GitHub.")
        return f"https://github.com/{username}/{repo_name}.git"
    else:
        print("Failed to create repository:", response.json())
        return None
        
def fake_repository(url, username):
    print("Faking " + url)
    git_url = 'https://github.com/' + username + '/' + url + '.git'
 
    os.system('git clone ' + git_url) # clone


    os.chdir(url)
    os.system('git branch -M main')
    os.system("""
                git filter-branch -f --env-filter \
                    "GIT_AUTHOR_NAME='{}'\
                     GIT_AUTHOR_EMAIL='{}'\
                     GIT_COMMITTER_NAME='{}'\
                     GIT_COMMITTER_EMAIL='{}'\
                     " HEAD\
                """.format(g_name, g_email, g_name, g_email))
    os.chdir('../')

    print(f"Success fake'{url}'\n ")


def push_repository(repos):
    print("Pushing " + repos)
    os.chdir(repos)
    os.system('git remote remove origin')
    os.system('git remote add origin https://github.com/{}/{}'.format(g_name, repos))
    os.system('git config user.name {}'.format(g_name))
    os.system('git config user.email {}'.format(g_email))
    os.system('git push -u origin main')
    os.chdir('../')

    print(f"Success push '{repos}'\n")


def get_public_repos(username):
    """
    Fetch the list of public repositories for a given GitHub username.
    """
    print(f"Fetching repositories for user '{username}'...\n")
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

if __name__ == '__main__':
    #############################################################
    ### Get repositories
    #############################################################

    for username in GITHUB_USERS : 

        public_repo_urls = get_public_repos(username)

        if not public_repo_urls:
            print("No repositories found or failed to fetch.")
            continue

        print(f"Found {len(public_repo_urls)} repositories.\n")

        print(f"Faking public repositories...")
        for repos in public_repo_urls:
            # test_github_token();
            create_github_new_repo(GITHUB_TOKEN, g_name, repos)

            # Get reopsitory name
            url_list = repos.split("/")
            repo_rul = url_list[4].replace("\n", "")
            
            repo_rul = repo_rul.replace(".git", "")
            print(f"Faking '{repo_rul}' repository...")
            fake_repository(repo_rul, username)
            push_repository(repo_rul)
            print(f"Faking '{repo_rul}' repository have been done.\n")

        print(f"Faking public repositories for '{username}' have been done.\n")

