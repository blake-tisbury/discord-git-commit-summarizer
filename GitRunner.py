# !/usr/bin/env python3
import asyncio
import datetime
import os
import requests
from dotenv import load_dotenv


class GitRunner:
    def __init__(self, repo_url: str, auth_token: str):
        self.repo_url = repo_url
        self.auth_token = auth_token
        self.repo_name = repo_url.split('/')[-1].split('.')[0]
        self.repo_owner = repo_url.split('/')[-2]

    async def get_commits(self, branch: str, num_days: int) -> list:
        # get commits from GitHub branch since input number of days

        # iso format is needed for the API
        # offset added for GitHub API?? I think this works
        date = (datetime.datetime.now() - datetime.timedelta(days=num_days, hours=3)).isoformat(timespec='minutes')

        print(datetime.datetime.now())

        url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits?sha={branch}&since={date}'
        headers = {'Authorization': f'token {self.auth_token}'}
        response = requests.get(url, headers=headers)
        commits = response.json()

        return commits

    async def get_branches(self) -> list:
        # get branches from GitHub repo

        url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/branches'
        headers = {'Authorization': f'token {self.auth_token}'}
        response = requests.get(url, headers=headers)
        branches = response.json()

        branches_list = []
        for branch in branches:
            branches_list.append(branch['name'])
        return branches_list


if __name__ == "__main__":
    # testing
    path = 'tokens.env'
    load_dotenv(dotenv_path=path, verbose=True)
    git_runner = GitRunner("https://github.com/blake-tisbury/sumo-man-game.git", os.getenv('GITHUB_TOKEN'))
    asyncio.run(git_runner.get_commits("main", 1))
