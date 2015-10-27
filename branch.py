'''base branch object'''

import os

import config

from repo import Repo


class Branch:

    def __init__(self, name):
        self.name = name

        self.repos = []

    def checkout_all_repos(self):
        repos_list = os.listdir(config.GIT_WD)

        for repo in repos_list:
            repo_inst = Repo(repo, self)

            has_branch = repo_inst.checkout()
            if has_branch:
                self.repos.append(repo_inst)
