'''base repository object'''

import os

import config

from page import Page
from common import git_cmd, copy_file


class File:

    def __init__(self, name, subpath):
        self.name = name
        self.subpath = subpath

class File_md(File):

    def __init__(self, name, subpath, num):
        self.name = name
        self.subpath = subpath
        self.num = num

class File_other(File):

    def __init__(self, name, subpath, repo_name, branch_name):
        self.name = name
        self.subpath = subpath
        self.repo_name = repo_name
        self.branch_name = branch_name

        if branch_name == config.MAIN_BRANCH:
            pre_dir = config.PUBLISH_DIR
        else:
            pre_dir = os.path.join(config.PUBLISH_DIR, branch_name)

        if repo_name == config.BASE_REPO_NAME:
            self.out_dir = os.path.join(pre_dir, subpath)
        else:
            self.out_dir = os.path.join(pre_dir, repo_name, subpath)

    def copy(self):
        in_filepath = os.path.join( config.GIT_WD,
                                    self.repo_name,
                                    self.subpath,
                                    self.name )
        copy_file(in_filepath, self.out_dir)


class Repo:

    def __init__(self, repo_name, branch_inst):
        self.name = repo_name
        self.branch = branch_inst

        self.md_files = []
        self.other_files = []

        self.pages = []

    def get_files_recurse(self, subpath=""):
        dir = os.path.join(config.GIT_WD, self.name, subpath)

        # get directory content
        dir_content_list = os.listdir(dir)

        # filter dir content
        md_file_num = 0
        subdirs = []
        for file in sorted(dir_content_list):
            if file.endswith(config.MD_EXT):
                file_inst = File_md(file, subpath, md_file_num)
                self.md_files.append(file_inst)
                md_file_num += 1

            elif os.path.isdir(os.path.join(dir, file)):
                subdirs.append(file)

            # more filters might be specified here
            # ...

            else:
                file_inst = File_other( file,
                                        subpath,
                                        self.name,
                                        self.branch.name )
                self.other_files.append(file_inst)

            # if no md file found, return (?)

        # remove excluded dirs
        # (debug print)
        #print("SUBDIRS LIST: ", subdirs_list)
        for excl_dir in config.EXCLUDE_DIRS:
            if excl_dir in subdirs:
                subdirs.remove(excl_dir)

        # recurse
        for subdir in subdirs:
            # the subdir needs to be:
            subpath_new=os.path.join(subpath, subdir)

            self.get_files_recurse(subpath_new)

    def load_pages(self):
        for md_file in self.md_files:
            page_inst = Page( self.branch,
                                self,
                                md_file.subpath,
                                md_file.name,
                                md_file.num )

            self.pages.append(page_inst)

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

    def copy_files(self):
        for file_inst in self.other_files:
            file_inst.copy()
