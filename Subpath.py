'''base subpath object'''

import os

import config

from File import File, File_md, File_other
from Page import Page
from nav_dir import gen_nav_path, gen_nav_dirlist

class Subpath:

    def __init__(self, name, repo, path=""):
        repo.subpaths.append(self)

        self.name = name
        self.repo = repo
        self.path = path

        self.nav_path = ""
        self.nav_dirlist = ""

        self.path_abs = os.path.join(config.GIT_WD, repo.name, path)

        self.files_md = []
        self.files_other = []
        self.subdirs = []

        self.pages = []
        self.active = False

        self.get_files()

        self.load_pages()

        self.set_description()

    def process(self):
        self.active = True
        # add path and directory list (not on base repo)
        if self.repo.name != config.BASE_REPO_NAME:
            self.nav_path = gen_nav_path(self)
#            self.nav_path = gen_nav_path( self.repo.branch.out_name,
#                                          self.repo.name,
#                                          self.path )
            self.nav_dirlist = gen_nav_dirlist(self)
#            self.nav_dirlist = gen_nav_dirlist( self.repo.branch.out_name,
#                                                self.repo.name,
#                                                self.path )

        for page in self.pages:
            page.process()
            page.write_out()

        self.active = False

    def get_files(self):
        # get directory content
        dir_content_list = os.listdir(self.path_abs)

        # filter dir content
        subdirs = []
        md_file_num = 0
        for file in sorted(dir_content_list):
            if file.endswith(config.MD_EXT):
                file_inst = File_md( file,
                                     self,
                                     md_file_num )
                self.files_md.append(file_inst)
                md_file_num += 1

            elif os.path.isdir(os.path.join(self.path_abs, file)):
                subdirs.append(file)

            # more filters might be specified here
            # ...

            else:
                file_inst = File_other( file,
                                        self )
                self.files_other.append(file_inst)

            # if no md file found, return (?)

        # remove excluded dirs
        for excl_dir in config.EXCLUDE_DIRS:
            if excl_dir in subdirs:
                subdirs.remove(excl_dir)

        # "recurse"
        for subdir in subdirs:
            subpath_inst = Subpath( subdir,
                                    self.repo,
                                    os.path.join(self.path, subdir) )
            self.subdirs.append(subpath_inst)

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

    def set_description(self):
        # try description file
        desc_filepath = os.path.join( self.path_abs,
                                      config.DIR_DESC_FILENAME )

        if os.path.isfile(desc_filepath):
            with open(desc_filepath, 'r') as f:
                self.desc = f.read()
            return

        # try the first md file
        elif self.pages != []:
            self.desc = self.pages[0].meta_title

        else:
            self.desc = "<pre>No description file or page available...</pre>"
