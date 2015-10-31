'''base file objects'''

import os

import config

class File:

    def __init__(self, name, subpath):
        self.name = name
        self.subpath = subpath
        self.repo = subpath.repo

class File_md(File):

    def __init__(self, name, subpath, num):
        super().__init__(name, subpath)
        self.num = num

        self.filepath = os.path.join( config.GIT_WD,
                                      self.repo.name,
                                      self.subpath.path,
                                      self.name )

class File_other(File):

    def __init__(self, name, subpath):
        super().__init__(name, subpath)
        self.branch_name = subpath.repo.branch.name
        self.repo_name = subpath.repo.name

        if self.branch_name == config.MAIN_BRANCH:
            pre_dir = config.PUBLISH_DIR
        else:
            pre_dir = os.path.join(config.PUBLISH_DIR, self.branch_name)

        if self.repo_name == config.BASE_REPO_NAME:
            self.out_dir = os.path.join(pre_dir, subpath.path)
        else:
            self.out_dir = os.path.join(pre_dir, self.repo_name, subpath.path)

    def copy(self):
        in_filepath = os.path.join( config.GIT_WD,
                                    self.repo_name,
                                    self.subpath.path,
                                    self.name )
        copy_file(in_filepath, self.out_dir)
