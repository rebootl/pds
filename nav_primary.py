'''primary navigation generation'''

import os

import config

from common import get_title

LI_HTML = '<li><a class="{}" href="{}">{}</a></li>\n'

def gen_nav_primary(branch):

    for repo in branch.repos:
        if repo.name == config.BASE_REPO_NAME:
            base_repo = repo

    menu = '<ul>\n'

    items = []
    branch_out = base_repo.branch.out_name

    # site index
    index_href = os.path.join('/', branch_out)
    link_text = base_repo.subpaths[0].pages[0].title
    if base_repo.subpaths[0].active:
        link_class = "active"
    else:
        link_class = ""

    li_item = LI_HTML.format(link_class, index_href, link_text)

    menu = menu + li_item

    # subdirs
    for subdir in base_repo.subpaths[0].subdirs:
        link_href = os.path.join('/', branch_out, subdir.name)
        link_text = subdir.pages[0].title
        if subdir.active:
            link_class = "active"
        else:
            link_class = ""

        li_item = LI_HTML.format(link_class, link_href, link_text)

        menu = menu + li_item

    menu = menu + '</ul>\n'

    return menu
