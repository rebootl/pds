'''directory navigation generation

shall be placed on every page, exept base-layout pages
(on my site it doesn't make sense on base-layout pages,
but it could be used there as well)
'''

import os

import config

A_HTML = '<a class="{}" href="{}">{}</a>'

def gen_nav_path(subpath):

    path_items = []
    path = subpath.path
    while path != '':
        path, subdir = os.path.split(path)
        if subdir != '':
            path_items.append(subdir)

    path_items.append(subpath.repo.out_name)
    path_items.reverse()

    nav_path = ""
    branch_out = subpath.repo.branch.out_name
    for n, item in enumerate(path_items):

        item_path = ""
        for i in range(n+1):
            item_path = os.path.join(item_path, path_items[i])

        link_href = os.path.join('/', branch_out, item_path)
        link = A_HTML.format("", link_href, item)

        nav_path = nav_path + link + ' / '

    return nav_path

# path = "2015-10-05/subdir/foo"
#
# path_items = [ "astro", "2015-10-05", "subdir", "foo" ]
#
#
#

LI_DESC_HTML = '<li><a class="{}" href="{}">{}</a><br />\n{}</li>\n'

def gen_nav_dirlist(subpath):

    menu = '<ul>\n'

    for subdir in reversed(subpath.subdirs):

        link_href = subdir.name
#        link_text = subdir.pages[0].meta_title

        li_item = LI_DESC_HTML.format("", link_href, link_href, subdir.desc)

        menu = menu + li_item

    menu = menu + '</ul>\n'

    return menu
