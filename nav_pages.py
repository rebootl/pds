'''navigation of pages in a directory'''

import os

import config

LI_HTML = '<li><a class="{}" href="{}">{}</a></li>\n'

def gen_nav_pagelist(subpath):

    # return empty if only one item
    if len(subpath.pages) < 2:
        return ""

    menu = '<ul>\n'

    for page in subpath.pages:

        link_href = page.out_filename
        link_text = page.title
        if page.active:
            link_active_class = 'active'
        else:
            link_active_class = ""

        li_item = LI_HTML.format(link_active_class, link_href, link_text)

        menu = menu + li_item

    # add list tags
    menu = menu + '</ul>\n'

    return menu
