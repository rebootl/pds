#!/usr/bin/python

import os

import config



def repos_list(branch):
    '''Return a list of repos w/ short-descriptions.'''

    # get the repos from git-wd
    repos_list=os.listdir(config.GIT_WD)

    # (filter base-repo)
    repos_list.remove(config.BASE_REPO_NAME)

    # (return if empty)
    if repos_list == []:
        return ""

    menu='<ul id="repos-list">\n'

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

    menu=menu+'</ul>\n'

    return menu, ""


def get_repo_desc(repo):

    desc_filepath=os.path.join(config.GIT_WD, repo, config.REPO_DESC_FILENAME)

    if os.path.isfile(desc_filepath):

        with open(desc_filepath, 'r') as f:
            description=f.read()
    else:
        description=""

    return description
