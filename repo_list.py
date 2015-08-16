import os

import config

#from menu import Menu
from common import get_title

def gen_repo_list(branch):
    '''Generate a list of repositories with descriptions.'''

    # get the repos from git-wd
    repos_list=os.listdir(config.GIT_WD)

    # filter out base-repo
    repos_list.remove(config.BASE_REPO_NAME)

    # return if empty
    if repos_list == []:
        return "No other repositories found yet..."

    menu='<ul>\n'
#    menu=menu+'<li>Repositories</li>\n'

    # add an item for every repo
    # (currently these do not receive an active class,
    #  but a description from desc-repo)
    # change: use dir name as title and markdown title as description
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

    return menu


def get_repo_desc(repo):
    '''get a repo/directory description text

if present use the description file
if not present use the title from the first markdown file
fallback to text
'''
    # try description file
    desc_filepath=os.path.join(config.GIT_WD, repo, config.REPO_DESC_FILENAME)

    if os.path.isfile(desc_filepath):
        with open(desc_filepath, 'r') as f:
            desc = f.read()
        return desc

    # try the first md file    
    repo_filepath_abs = os.path.join(config.GIT_WD, repo)

    repo_files = os.listdir(repo_filepath_abs)

    first_md_file = ""
    for file in sorted(repo_files):
        if file.endswith(config.MD_EXT):
            first_md_file = file
            break

    if first_md_file == "":
        return "No description (markdown file) available, yet..."

    md_filepath_abs = os.path.join(repo_filepath_abs, first_md_file)

    desc = get_title(md_filepath_abs)

    if desc == "":
        return "No description (page title) available..."

    return desc
