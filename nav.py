#!/usr/bin/python
'''Primary functions to generate the navigation.'''

import os

import config

from custom_nav import base_nav_list, repos_nav_list
from common import get_title
from menu import Menu

def primary_nav(branch, active_path):
    '''Generate the (custom) primary navigation.

Containing base_nav_list and repos_nav_list.
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
    menu=menu+repos_nav_list(branch)
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

        if active_reldir != "":
            menu_inst=Menu(branch, repo_name, active_path, active_reldir)
            menu=menu_inst.menu
        else:
            return ""

    else:

        menu='<h2>Repository:</h2>\n<h3>{}</h3>\n'.format(repo_name)
        menu_inst=Menu(branch, repo_name, active_path)
        menu=menu+menu_inst.menu

    return menu
