'''base branch object'''

import os

import config

from Repo import Repo


class Branch:

    def __init__(self, name):
        self.name = name

        # the main branch shall not go in a subdirectory
        # therefor setting to out name here
        if self.name == config.MAIN_BRANCH:
            self.out_name = ""
        else:
            self.out_name = self.name

        self.repos = []

        self.initialize_repos()

        # (has to be done after loading)
        self.process_repos()

    def initialize_repos(self):
        '''checkout and load repositories'''
        repos_list = os.listdir(config.GIT_WD)

        for repo in repos_list:
            repo_inst = Repo(repo, self)

    def process_repos(self):
        for repo in self.repos:
            repo.process()
