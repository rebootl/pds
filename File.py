'''base file objects'''

import os

import config

from common import copy_file

class File:

    def __init__(self, name, subpath):
        self.name = name
        self.subpath = subpath
        self.repo = subpath.repo

        self.filepath = os.path.join( config.GIT_WD,
                                      subpath.repo.name,
                                      subpath.path,
                                      self.name )

class File_md(File):

    def __init__(self, name, subpath, num):
        super().__init__(name, subpath)
        self.num = num

class File_other(File):

    def __init__(self, name, subpath):
        super().__init__(name, subpath)

        self.out_dir = os.path.join( config.PUBLISH_DIR,
                                     subpath.repo.branch.out_name,
                                     subpath.repo.out_name,
                                     subpath.path )

    def copy(self):
        copy_file(self.filepath, self.out_dir)
