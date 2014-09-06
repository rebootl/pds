#!/usr/bin/python


import os

import config

from common import get_title


class Menu:

    def __init__(self, branch, repo_name, active_path, curr_subdir=""):

        self.branch=branch
        self.repo_name=repo_name
        self.active_path=active_path
        # (starting subdir)
        self.curr_subdir=curr_subdir
        if repo_name == config.BASE_REPO_NAME:
            self.pre_dir=""
        else:
            self.pre_dir=repo_name
        # (starting tag)
        self.menu=""
        # (link counter)
        self.link_cnt=0

        self.generate_menu_recurse()


    def generate_menu_recurse(self):

        self.menu=self.menu+'<ul>\n'

        # (get dir content)
        dir_abs=os.path.join(config.GIT_WD, self.repo_name, self.curr_subdir)

        dir_content=os.listdir(dir_abs)
        dir_content.sort()

        file_num=0
        for file in dir_content:

            filepath_abs=os.path.join(dir_abs, file)

            if file.endswith(config.MD_EXT):

                self.make_link_entry(file_num, file, filepath_abs)
                # (need to count in here)
                file_num+=1

            elif os.path.isdir(filepath_abs) and file not in config.EXCLUDE_DIRS:

                self.menu=self.menu+'<li>'+file+'/'

                # (re-set current subdir)
                subdir_path_rel=os.path.relpath(filepath_abs, os.path.join(config.GIT_WD, self.repo_name))
                self.curr_subdir=subdir_path_rel

                # (recurse)
                self.generate_menu_recurse()

                self.menu=self.menu+'</li>\n'

        self.menu=self.menu+'</ul>\n'


    def make_link_entry(self, file_num, filename_md, filepath_abs):

        # count the links
        self.link_cnt=self.link_cnt+1

        # set the href
        if file_num == 0:
            filename="index.html"
        else:
            filename_noext=os.path.splitext(filename_md)[0]
            filename=filename_noext+".html"

        # (using os.path.abspath does not work here)
        link_href=os.path.join('/', self.branch, self.pre_dir, self.curr_subdir, filename)

        # set the link text
        # (get the page title from Pandoc title block)
        link_text=get_title(filepath_abs)

        # set active class
        if filepath_abs == self.active_path:
            link_class='class="active"'
        else:
            link_class=""

        # create link
        link_line='<li><a {} href="{}">{}</a></li>\n'.format(link_class, link_href, link_text)

        self.menu=self.menu+link_line

