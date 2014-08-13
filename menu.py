


import os

import config

from common import read_tb_lines



class Menu:

    def __init__(self, branch, repo_name, active_path):

        self.branch=branch
        self.repo_name=repo_name
        self.active_path=active_path
        # (starting subdir)
        self.curr_subdir=""
        if repo_name == config.BASE_REPO_NAME:
            self.pre_dir=""
        else:
            self.pre_dir=repo_name
        # (starting tag)
        self.menu='<ul>\n'

        self.generate_menu_recurse()


    def generate_menu_recurse(self):

        # (get dir content)
        self.dir_abs=os.path.join(config.GIT_WD, self.repo_name, self.curr_subdir)
        print(self.dir_abs)
        dir_content=os.listdir(self.dir_abs)
        dir_content.sort()
        print(dir_content)
        for file_num, file in enumerate(dir_content):

            if file.endswith(config.MD_EXT):
                self.make_entry_link(file, file_num)

            elif os.path.isdir(os.path.join(self.dir_abs, file)) and file not in config.EXCLUDE_DIRS:
                # create submenu

                self.menu=self.menu+'<li>'+file+'/'

                # (re-set current subdir)
                subdir_path_abs=os.path.join(self.dir_abs, self.curr_subdir)
                subdir_path_rel=os.path.relpath(subdir_path_abs, os.path.join(config.GIT_WD, self.repo_name))
                self.curr_subdir=subdir_path_rel

                # (recurse)
                submenu=self.generate_menu_recurse()

                self.menu=self.menu+submenu+'</li>'

        self.menu=self.menu+'</ul>'


    def make_entry_link(self, filename_md, file_num):

        filename_noext=os.path.splitext(filename_md)[0]

        # set the href

        if file_num == 0:
            filename="index.html"
        else:
            filename=filename_noext+".html"

        # --> use os.absdir (?) here
        link_href="/"+os.path.join(self.pre_dir, self.curr_subdir, filename)

        # set the link text

        # (get the page title from Pandoc title block)
        filepath_abs=os.path.join(self.dir_abs, filename_md)
        # --> only read title here
        tb_title_list=read_tb_lines(filepath_abs)
        if tb_title_list == []:
            # (use the filename as fallback)
            link_text=filename_noext
        else:
            link_text=tb_title_list[0]

        # set active class
        if filepath_abs == self.active_path:
            link_class='class="active"'
        else:
            link_class=""

        # create link
        link_line='<li><a {} href="{}">{}</a></li>\n'.format(link_class, link_href, link_text)

        self.menu=self.menu+link_line



def generate_base_menu(branch, active_path):

    base_menu_inst = Menu(branch, config.BASE_REPO_NAME, active_path)
    base_menu=base_menu_inst.menu

    return base_menu


def generate_repos_menu(branch, active_path):

    # get all repos
    repos_list=os.listdir(config.GIT_WD)

    # filter out the "base" repo
    repos_list.remove(config.BASE_REPO_NAME)

    menu=""
    # generate the menu
    for repo in sorted(repos_list):

        if repo in active_path:
            active_id="span-arrow-active"
        else:
            active_id=""

        menu=menu+'<h3 onclick="javascript:show_menu(this, \'repo-menu-{repo_name}\')">{repo_name}<span class=\"arrow\" id=\"{id}\"></span></h3>\n'.format(repo_name=repo, id=active_id)

        #menu=menu+generate_menu_recurse(branch, repo, active_path, "repo-menu")

        repo_menu_inst = Menu(branch, repo, active_path)
        repo_menu=menu+repo_menu_inst.menu

    return repo_menu
