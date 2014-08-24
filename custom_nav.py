#!/usr/bin/python
'''Custom functions to generate the navigation.'''

import os

import config

from menu import Menu


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


def repos_nav_list(branch):
    '''Generate a list of repositories with descriptions.'''

    # get the repos from git-wd
    repos_list=os.listdir(config.GIT_WD)

    # (filter base-repo)
    repos_list.remove(config.BASE_REPO_NAME)

    # (return if empty)
    if repos_list == []:
        return ""

    menu='<li id="repos-list"><a href="#">Repositories</a><ul>\n'
#    menu=menu+'<li>Repositories</li>\n'

    # add an item for every repo
    # (currently these do not receive an active class,
    #  but a description from desc-repo)
    for repo in repos_list:

        # (these links go to the repo/index.html)
        link_src=os.path.join('/', branch, repo, "index.html")

        link_text=repo

        desc=get_repo_desc(repo)
        if desc != "":
            link_desc='<br />'+desc
        else:
            link_desc=""

        menu=menu+'<li><a href="{}">{}</a>{}</li>\n'.format(link_src, link_text, link_desc)

    menu=menu+'</ul></li>\n'

    return menu


def get_repo_desc(repo):

    desc_filepath=os.path.join(config.GIT_WD, repo, config.REPO_DESC_FILENAME)

    if os.path.isfile(desc_filepath):

        with open(desc_filepath, 'r') as f:
            description=f.read()
    else:
        description=""

    return description
