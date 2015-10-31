'''repository list generation'''

import os

import config

#from menu import Menu
from common import get_title

def repo_list(branch):
    '''generate a list of repositories with descriptions'''

    # get the repos from git-wd
#    repos_list=os.listdir(config.GIT_WD)
    repos_list = branch.repos.copy()

    # filter out base-repo
    for repo in repos_list:
        if repo.name == config.BASE_REPO_NAME:
            repos_list.remove(repo)

    # return if empty
    if repos_list == []:
        return "<pre>No other repositories found yet...</pre>"

    menu='<ul>\n'
#    menu=menu+'<li>Repositories</li>\n'

    # add an item for every repo
    # (currently these do not receive an active class,
    #  but a description from desc-repo)
    # change: use dir name as title and markdown title as description
    for repo in repos_list:

        # (these links go to the repo/index.html)
        link_src = os.path.join('/', branch.out_name, repo.name, "index.html")

        link_text = repo.name

        desc = repo.desc

        if desc != "":
            link_desc = '<br />' + desc
        else:
            link_desc = ""

        menu = menu + '<li><a href="{}">{}</a>{}</li>\n'.format(link_src, link_text, link_desc)

    menu = menu + '</ul>\n'

    return "", "", [ '--variable=repo-list:'+menu ]
