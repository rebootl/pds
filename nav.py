#!/usr/bin/python
'''Primary functions to generate the navigation.'''

import os

import config

from custom_nav import base_nav_list, repos_nav_list
from common import get_title

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

    menu=menu+'<li><a {} href="{}">{}</a></li>'.format(active_class, index_href, link_text)

    # additional items (subdirectories)
    menu=menu+base_nav_list(branch, active_path)
    # repos sublist item
    menu=menu+repos_nav_list(branch)+'</ul>\n'

    return menu


def secondary_nav(branch, active_path):
    '''Generate the (custom) secondary navigation.

Creates a Menu for the __active__ directory.
'''

    return ""
