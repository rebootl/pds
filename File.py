'''base file objects'''

import os

import config

class File:

    def __init__(self, name, subpath):
        self.name = name
        self.subpath = subpath

class File_md(File):

    def __init__(self, name, subpath, num):
        super().__init__(name, subpath)
        self.num = num

class File_other(File):

    def __init__(self, name, subpath, repo_name, branch_name):
        super().__init__(name, subpath)
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
