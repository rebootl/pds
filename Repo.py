'''repository object'''

import os

import config

from common import git_cmd, copy_file

from Subpath import Subpath


class Repo:

    def __init__(self, name, branch):
        self.name = name
        self.branch = branch

        self.path_abs = os.path.join(config.GIT_WD, self.name)

        has_branch = self.checkout()
        if has_branch:
            self.branch.repos.append(self)
        else:
            return

        if self.name == config.BASE_REPO_NAME:
            self.out_name = ""
        else:
            self.out_name = self.name

        # load files, subdirs and pages, "recursive",
        # (write back subpaths)
        self.subpaths = []
        self.subpath = Subpath("repo-root", self)

#        self.load()

        # (has to be done after loading)
        self.desc = self.subpaths[0].desc

#        if self.name == config.BASE_REPO_NAME:
#            self.branch.nav_primary_items = gen_nav_primary_items(self)

#    def load(self):
#        '''load files, subdirs and pages, recursive'''
#        self.subpath = Subpath(self)

    def process(self):
        for subpath in self.subpaths:
            subpath.process()

# --> mv this back to git functions
    def checkout(self):
        oldwd = os.getcwd()
        os.chdir( os.path.join(config.GIT_WD, self.name) )
        # (checkout)
        # --> evtl. make this nicer e.g. check if branch exists
        # (info print)
        print('pds: repo: "{}"'.format(self.name))

        ret = git_cmd("checkout", [ self.branch.name ])
        if ret == 0:
            # (add to return list)
            has_branch = True
        else:
            has_branch = False
            print('pds: repo "{}" has no branch "{}"'.format( self.name,
                                                              self.branch.name ))

        # (update the branch)
        # --> evtl. also make this nicer e.g. check if up-to-date
        # (info print)
        #print("pds: update repo: ", repo)
        git_cmd("pull")
        os.chdir(oldwd)

        return has_branch

#    def copy_files(self):
#        for file_inst in self.other_files:
#            file_inst.copy()
