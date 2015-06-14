#!/usr/bin/python
'''Primary functions to generate the navigation.'''

import os

import config

from common import get_title
from menu import Menu

def primary_nav(branch, active_path):
    '''Generate the primary navigation.

Containing the main items of the base-layout.
'''

    # index.html
    menu='<ul>\n'
    # (link to site index.html)
    index_href=os.path.join('/', branch)
    # (when in base-repo directory, this shall be active)
    print("active_path: ", active_path)

    # get the link text
    dir=os.path.join(config.GIT_WD, config.BASE_REPO_NAME)
    dir_content=os.listdir(dir)
    dir_content.sort()
    for file in dir_content:
        if file.endswith(config.MD_EXT):
            filepath_abs=os.path.join(dir, file)
            link_text=get_title(filepath_abs)
            break

    if os.path.basename(os.path.dirname(active_path)) == config.BASE_REPO_NAME:
        active_class='class="active"'
    else:
        active_class=""

    menu=menu+'<li><a {} href="{}">{}</a></li>\n'.format(active_class, index_href, link_text)

    # additional items (subdirectories)
    menu=menu+base_nav_list(branch, active_path)
    # repos sublist item
    # --> repos shall be done separately
#    menu=menu+repos_nav_list(branch)
    #menu=menu+'<li>Repositories</li>'

    menu=menu+'</ul>\n'

    return menu


def secondary_nav(branch, repo_name, active_path):
    '''Generate the (custom) secondary navigation.

For the base-layout it'll create a full menu for the active subdirectory.
For the other repos it'll create a full menu for the active repository.
'''

    if repo_name == config.BASE_REPO_NAME:

        active_relpath=os.path.relpath(active_path, os.path.join(config.GIT_WD, config.BASE_REPO_NAME))
        #print("active_relpath: ", active_relpath)
        active_reldir=os.path.dirname(active_relpath)
        #print("active_reldir: ", active_reldir)

        if active_reldir == "":
            return ""

        menu_inst=Menu(branch, repo_name, active_path, active_reldir)
        if menu_inst.link_cnt <= 1:
            return ""
        else:
            menu=menu+menu_inst.menu

    else:

#        menu='<h2>Repository:</h2>\n<h3>{}</h3>\n'.format(repo_name)
        menu='<h3>{}</h3>\n'.format(repo_name)
        menu_inst=Menu(branch, repo_name, active_path)
        menu=menu+menu_inst.menu

    return menu


def base_nav_list(branch, active_path):
    '''Generate the base navigation.

Contains base-layout items (directories)
'''

    # base-layout items
    dir=os.path.join(config.GIT_WD, config.BASE_REPO_NAME)
    dir_content=os.listdir(dir)

    menu=""

    for file in dir_content:

        filepath_abs=os.path.join(dir, file)

        if os.path.isdir(filepath_abs) and file not in config.EXCLUDE_DIRS:

            # (href)
            link_href=os.path.join('/', branch, file)

            # (link text)
            # --> the link text is the filename

            # (active class)
            if filepath_abs in active_path:
                link_class='class="active"'
            else:
                link_class=""

            menu=menu+'<li><a {} href="{}">{}</a></li>\n'.format(link_class, link_href, file)

    return menu
