'''base subpath object'''

import os

import config

from File import File, File_md, File_other
from Page import Page
from nav_dir import gen_nav_path, gen_nav_dirlist

class Subpath:

    def __init__(self, repo, path=""):
        repo.subpaths.append(self)

        self.repo = repo
        self.path = path

# --> todo set
#        self.desc = desc
        self.nav_path = ""
        self.nav_dirlist = ""

        self.path_abs = os.path.join(config.GIT_WD, repo.name, path)

        self.files_md = []
        self.files_other = []
        self.subdirs = []

        self.pages = []

        self.get_files()

        self.load_pages()

    def process(self):
        # add path and directory list (not on base repo)
        if self.repo.name != config.BASE_REPO_NAME:
            self.nav_path = gen_nav_path( self.repo.branch.out_name,
                                          self.repo.name,
                                          self.path )
            self.nav_dirlist = gen_nav_dirlist( self.repo.branch.out_name,
                                                self.repo.name,
                                                self.path )

        for page in self.pages:
            page.process()
            page.write_out()

    def get_files(self):
        # get directory content
        dir_content_list = os.listdir(self.path_abs)

        # filter dir content
        md_file_num = 0
        for file in sorted(dir_content_list):
            if file.endswith(config.MD_EXT):
                file_inst = File_md( file,
                                     self,
                                     md_file_num )
                self.files_md.append(file_inst)
                md_file_num += 1

            elif os.path.isdir(os.path.join(self.path_abs, file)):
                self.subdirs.append(file)

            # more filters might be specified here
            # ...

            else:
                file_inst = File_other( file,
                                        self )
                self.files_other.append(file_inst)

            # if no md file found, return (?)

        # remove excluded dirs
        # (debug print)
        #print("SUBDIRS LIST: ", subdirs_list)
        for excl_dir in config.EXCLUDE_DIRS:
            if excl_dir in self.subdirs:
                self.subdirs.remove(excl_dir)

        # "recurse"
        for subdir in self.subdirs:
            subpath_inst = Subpath( self.repo,
                                    os.path.join(self.path, subdir) )

    def load_pages(self):
        for file_md in self.files_md:
            page_inst = Page( self.repo.branch,
                              self.repo,
                              self,
                              file_md )

            self.pages.append(page_inst)

# --> what was this for ?
#            # add subdir instance w/ description (only for first md file)
#            if md_file.num == 0:
#                subdir_inst = Subdir( self.subpath,
#                                      page_inst.meta_title )
#
#                self.subdirs.append(subdir_inst)

    def copy_files(self):
        for file_inst in self.other_files:
            file_inst.copy()
