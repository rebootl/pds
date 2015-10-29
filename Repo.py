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

        # this initiates loading of files and subdirectories
        self.subpath = Subpath( self )

        self.set_description()

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

#    def get_files_recurse(self, subpath=""):
#        dir = os.path.join(config.GIT_WD, self.name, subpath)
#
#        # get directory content
#        dir_content_list = os.listdir(dir)
#
#        # filter dir content
#        md_file_num = 0
#        subdirs = []
#        for file in sorted(dir_content_list):
#            if file.endswith(config.MD_EXT):
#                file_inst = File_md(file, subpath, md_file_num)
#                self.md_files.append(file_inst)
#                md_file_num += 1
#
#            elif os.path.isdir(os.path.join(dir, file)):
#                subdirs.append(file)
#
#            # more filters might be specified here
#            # ...
#
#            else:
#                file_inst = File_other( file,
#                                        subpath,
#                                        self.name,
#                                        self.branch.name )
#                self.other_files.append(file_inst)
#
#            # if no md file found, return (?)
#
#        # remove excluded dirs
#        # (debug print)
#        #print("SUBDIRS LIST: ", subdirs_list)
#        for excl_dir in config.EXCLUDE_DIRS:
#            if excl_dir in subdirs:
#                subdirs.remove(excl_dir)
#
#        # recurse
#        for subdir in subdirs:
#            # the subdir needs to be:
#            subpath_new=os.path.join(subpath, subdir)
#
#            self.get_files_recurse(subpath_new)

#    def load_pages(self):
#        for md_file in self.md_files:
#            page_inst = Page( self.branch,
#                                self,
#                                md_file.subpath,
#                                md_file.name,
#                                md_file.num )
#
#            self.pages.append(page_inst)
#
#            # add subdir instance w/ description (only for first md file)
#            if md_file.num == 0:
#                subdir_inst = Subdir( self.subpath,
#                                      page_inst.meta_title )
#
#                self.subdirs.append(subdir_inst)

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
