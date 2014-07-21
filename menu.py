
# Menu generation workflow
# ------------------------
#
# The goal would be to generate the menus only once and reuse it
# for the different pages.
#
# The idea to accomplish this would be to use a class for menus.
# An instance should be created on global level, but nothing
# should be generated at this point, since we first need to refresh
# all the repos. (Therefor not using __init__.)
# The class should provide a method to 'get' the respective menu.
# This method should return the menu, creating it if it doesn't
# exist yet.

import os

import config

from common import read_tb_lines

def generate_menu_subpath(branch, repo_name, subpath, active_path):

    # for the "base" menu we don't want to have the directory
    # name in the path, but for the "repo"/other menus we do
    if repo_name == config.BASE_REPO_NAME:
        pre_dir=""
    else:
        pre_dir=repo_name

    dir=os.path.join(config.GIT_WD, repo_name, subpath)

    dir_content=os.listdir(dir)

    md_files=[]
    for file in dir_content:
        if file.endswith(config.MD_EXT):
            md_files.append(file)

    # filter
    for file in md_files:
        for keyword in config.MENU_EXCLUDE_FILES_MD:
            if keyword in file:
                md_files.remove(file)

    link_line_templ='<li><a {} href="{}">{}</a></li>\n'

    # generate the menu entries
    dir_menu=""
    for idx, md_file in enumerate(sorted(md_files)):

        filename_noext=os.path.splitext(md_file)[0]

        # get the page title from Pandoc title block
        full_filepath=os.path.join(dir, md_file)
        tb_title_list=read_tb_lines(full_filepath)
        print("TB TITLE LIST: ", tb_title_list)

        if tb_title_list == []:
            # (use the filename as fallback)
            page_title=filename_noext
        else:
            page_title=tb_title_list[0]

        # set the src name
        if idx == 0:
            src_name="index.html"
        else:
            src_name=filename_noext+".html"

        if full_filepath == active_path:
            active_class='class="active"'
        else:
            active_class=""

        link_src="/"+os.path.join(branch, pre_dir, subpath, src_name)

        link_line=link_line_templ.format(active_class, link_src, page_title)

        dir_menu=dir_menu+link_line

    return dir_menu



def generate_menu_recurse(branch, repo_name, active_path, dir=""):

    # (tags)
    tag_dir="<li>{}</li>\n"

    # (get md links)
    menu="<ul>\n"+generate_menu_subpath(branch, repo_name, dir, active_path)

    # (dir content)
    dir_abs=os.path.join(config.GIT_WD, repo_name, dir)

    dir_content=os.listdir(dir_abs)

    subdirs=[]
    for file in dir_content:
        filepath=os.path.join(dir_abs, file)
        if os.path.isdir(filepath):
            subdirs.append(file)
    #print("SUBDIRS: ", subdirs)

    for excl_dir in config.EXCLUDE_DIRS:
        if excl_dir in subdirs:
            subdirs.remove(excl_dir)

    #print("SUBDIRS: ", subdirs)
    for subdir in subdirs:
            subdir_path_abs=os.path.join(dir_abs, subdir)
            # (add entry for directory)
            menu=menu+tag_dir.format(subdir+"/")

            subdir_path_rel=os.path.relpath(subdir_path_abs, os.path.join(config.GIT_WD, repo_name))
     #       print("SUBDIR PATH REL: ", subdir_path_rel)
            menu=menu+generate_menu_recurse(branch, repo_name, active_path, subdir_path_rel)

    # (add closing tag)
    menu=menu+"</ul>\n"

    return menu


def generate_base_menu(branch, active_path):

    base_menu=generate_menu_recurse(branch, config.BASE_REPO_NAME, active_path)

    return base_menu


def generate_repos_menu(branch, active_path):

    # get all repos
    repos_list=os.listdir(config.GIT_WD)

    # filter out the "base" repo
    repos_list.remove(config.BASE_REPO_NAME)

    menu=""
    # generate the menu
    for repo in sorted(repos_list):
        menu=menu+"<h3>"+repo+"</h3>\n"#<ul>\n"
        menu=menu+generate_menu_recurse(branch, repo, active_path)
#        menu=menu+"</ul>\n"

    return menu


class Menu:
    
    def __init__(self, type="base"):

        self.generated=False
        self.type=type
        self.menu=""

    def get_menu():

        if self.generated:
            return self.menu
        else:
            self.gen_menu()
            return self.menu

    def gen_menu():

        if self.type == "base":
            self.menu=generate_base_menu()
            self.generated=True

        elif self.type == "repos":
            self.menu=generate_repo_menu()
            self.generated=True

        else:
            print("Menu: Bad menu type, leaving.")


#base_menu=Menu("base")
