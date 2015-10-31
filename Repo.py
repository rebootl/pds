'''base repository object'''

import os

import config

from common import git_cmd, copy_file

from Subpath import Subpath
from Page import Page

class Repo:

    def __init__(self, name, branch):
        self.name = name
        self.branch = branch

        self.path_abs = os.path.join(config.GIT_WD, self.name)
        self.subpaths = []

        has_branch = self.checkout()
        if has_branch:
            self.branch.repos.append(self)

        self.load()

        # (has to be done after loading)
        self.set_description()

    def process(self):
        for subpath in self.subpaths:
            subpath.process()


    def load(self):
        '''load files, subdirs and pages, recursive'''
        self.subpath = Subpath(self)

    def set_description(self):
        # try description file
        desc_filepath = os.path.join( self.path_abs,
                                      config.REPO_DESC_FILENAME )

        if os.path.isfile(desc_filepath):
            with open(desc_filepath, 'r') as f:
                self.desc = f.read()
            return

        # try the first md file
        elif self.subpath.pages:
            self.desc = self.subpath.pages[0].meta_title

        else:
            self.desc = "<pre>No description file or page available...</pre>"

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
