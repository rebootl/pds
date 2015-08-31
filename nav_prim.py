'''primary navigation generation'''

import os

import config

from common import get_title, get_dir_desc
#from menu import Menu

def gen_nav_primary(branch, active_path):
    '''generate the primary navigation

using the main items of the base-layout:

- the site index.html (first markdown file from the base-layout)
  showing it's markdown title
- the base-layout subdirectories
  showing the directory name
  --> could/should be improved to show the markdown title
'''
    # start list
    menu = '<ul>\n'

    # site index.html
    menu = menu + add_menu_site_index(branch, active_path)

    # add subdirectories
    menu = menu + add_menu_subdirs(branch, active_path)

    # end list
    menu = menu+'</ul>\n'

    return menu


def add_menu_site_index(branch, active_path):
    '''helper to primary_nav

add the site index.html to HTML list
'''
    # link to site index.html
    index_href = os.path.join('/', branch)

    # get the link text from markdown title
    dir = os.path.join(config.GIT_WD, config.BASE_REPO_NAME)

    link_text = get_first_title(dir)

    # when in base-repo directory, this shall be active
    if os.path.basename(os.path.dirname(active_path)) == config.BASE_REPO_NAME:
        active_class = 'class="active"'
    else:
        active_class = ""

    list_html = '<li><a {} href="{}">{}</a></li>\n'.format(active_class, index_href, link_text)

    return list_html


def add_menu_subdirs(branch, active_path):
    '''helper to primary_nav

add base-layout subdirectories to HTML list
'''
    # base-layout items
    dir = os.path.join(config.GIT_WD, config.BASE_REPO_NAME)
    dir_content = os.listdir(dir)

    list_html = ''

    for file in dir_content:

        filepath_abs = os.path.join(dir, file)

        if os.path.isdir(filepath_abs) and file not in config.EXCLUDE_DIRS:

            link_href = os.path.join('/', branch, file)

            link_text = get_first_title(filepath_abs)

            # (active class)
            if filepath_abs in active_path:
                link_class = 'class="active"'
            else:
                link_class = ""

            list_html = list_html + '<li><a {} href="{}">{}</a></li>\n'.format(link_class, link_href, link_text)

    return list_html


def get_first_title(dir_abs):
    '''get the title from the first markdown file in dir

using get_title'''
    dir_content = os.listdir(dir_abs)
    for file in sorted(dir_content):
        if file.endswith(config.MD_EXT):
            filepath_abs = os.path.join(dir_abs, file)
            link_text = get_title(filepath_abs)
            break
    return link_text
