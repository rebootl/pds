'''repository object'''

import os

import config

from Subpath import Subpath
from git_processing import checkout_repo


class Repo:

    def __init__(self, name, branch):
        self.name = name
        self.branch = branch

        self.path_abs = os.path.join(config.GIT_WD, self.name)

        has_branch = checkout_repo(self)
        if has_branch:
            self.branch.repos.append(self)
        else:
            return

        if self.name == config.BASE_REPO_NAME:
            self.out_name = ""
        else:
            self.out_name = self.name

        # load files, subdirs and pages, "recursive",
        # (writes back subpaths)
        self.subpaths = []
        self.subpath = Subpath("repo-root", self)

        # (has to be done after loading)
        self.desc = self.subpaths[0].desc

    def process(self):
        for subpath in self.subpaths:
            subpath.process()

#    def copy_files(self):
#        for file_inst in self.other_files:
#            file_inst.copy()
