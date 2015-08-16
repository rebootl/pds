'''repository list generation'''

import os

import config

#from menu import Menu
from common import get_title, get_dir_desc

def gen_repo_list(branch):
    '''generate a list of repositories with descriptions'''

    # get the repos from git-wd
    repos_list=os.listdir(config.GIT_WD)

    # filter out base-repo
    repos_list.remove(config.BASE_REPO_NAME)

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
        link_src = os.path.join('/', branch, repo, "index.html")

        link_text = repo

        desc = get_dir_desc(os.path.join(config.GIT_WD, repo))

        if desc != "":
            link_desc = '<br />' + desc
        else:
            link_desc = ""

        menu = menu + '<li><a href="{}">{}</a>{}</li>\n'.format(link_src, link_text, link_desc)

    menu = menu + '</ul>\n'

    return menu
