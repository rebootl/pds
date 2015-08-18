'''directory navigation generation

shall be placed on every page, exept base-layout pages
(on my site it doesn't make sense on base-layout pages,
but it could be used there as well)
'''

import os

import config

from common import get_title, get_dir_desc
#from menu import Menu

def gen_nav_path(branch, repo_name, subpath, active_path):
    '''generate a navigation path

<current_repo> / <active_subdirs>
'''
    link_html = '<a class="Directory" href="{}">{}</a>'

    if repo_name == config.BASE_REPO_NAME:
        href_path_pre = os.path.join('/', branch, subpath)
    else:
        href_path_pre = os.path.join('/', branch, repo_name, subpath)

    # generate path items
    path_items = [ repo_name ]
    path = subpath
    while True:
        path, subdir = os.path.split(path)
        if subdir != '':
            path_items.append(subdir)
        elif path == '': break

    # (debug print)
    print("path items: ", path_items)

    if repo_name == config.BASE_REPO_NAME:
        path_items = path_items[1:]

    nav_path = ''
    for idx, item in enumerate(path_items):
        href_path = os.path.join((len(path_items)-idx) * '../', item)

        nav_path = nav_path + '<a class="Directory" href="{}">{}</a>'.format(href_path, item) + ' / '

    print("nav path: ", nav_path)

    return nav_path


def gen_nav_dirlist(branch, repo_name, subpath, active_path):
    '''generate a of the current directory content,

- markdown files
- subdirectories
'''
    # start list
    menu = '<ul>\n'

    # get directory content
    dir_path_abs = os.path.join(config.GIT_WD, repo_name, subpath)

    dir_content = os.listdir(dir_path_abs)

    # get markdown files and subdirectories
    md_files = []
    subdirs = []
    for file in sorted(dir_content):
        filepath_abs = os.path.join(dir_path_abs, file)
        if file.endswith(config.MD_EXT):
            md_files.append(file)
        elif os.path.isdir(filepath_abs) and file not in config.EXCLUDE_DIRS:
            subdirs.append(file)

    if repo_name == config.BASE_REPO_NAME:
        href_path_pre = os.path.join('/', branch, subpath)
    else:
        href_path_pre = os.path.join('/', branch, repo_name, subpath)

    # add markdown files
    menu = menu + add_md_files(dir_path_abs, href_path_pre, md_files)

    # add subdirectories with description
    menu = menu + add_subdirs(dir_path_abs, href_path_pre, subdirs)

    # end menu
    menu = menu + '</ul>\n'

    return menu


def add_md_files(dir_path_abs, href_path_pre, md_files):
    '''helper function to gen_dir_nav

add md files to HTML list'''
    list_html = ''
    # (don't set active class for now)
    link_class = ''
    for num, filename_md in enumerate(md_files):
        if num == 0:
            filename = "index.html"
        else:
            filename_noext = os.path.splitext(filename_md)[0]
            filename = filename_noext + ".html"

        link_href = os.path.join(href_path_pre, filename)

        link_text = get_title(os.path.join(dir_path_abs, filename_md))
        # (use filename as fallback)
        if link_text == '' and 'filename_noext' in locals():
            link_text = filename_noext
        elif link_text == '':
            link_text = os.path.splitext(filename_md)[0]

        list_html = list_html + '<li><a {} href="{}">{}</a></li>\n'.format(link_class, link_href, link_text)

    return list_html


def add_subdirs(dir_path_abs, href_path_pre, subdirs):
    '''helper function to gen_dir_nav

add subdirectories with descriptions to HTML list'''
    list_html = ''
    # (don't set active class for now)
    link_class = ''
    for subdir in subdirs:
        link_href = os.path.join(href_path_pre, subdir)

        list_html = list_html + '<li><a {} href="{}">{}</a><br />\n'.format(link_class, link_href, subdir+'/')

        desc = get_dir_desc(os.path.join(dir_path_abs, subdir))

        list_html = list_html + desc + '</li>\n'

    return list_html
