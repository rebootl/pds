#!/usr/bin/python
'''a personal documentation system or...

...a git based static website generator'''
#
#
#
#

# Per website settings

# the branches to process
DEF_BRANCHES=[ "public", "private", "preview" ]

# the repository path
REPO_DIR="/home/cem/website/repos"

# the publish directory
PUBLISH_DIR="/home/cem/website/http-serv"

# pandoc title block lines
TB_LINES=['title', 'author', 'date']
#TB_LINES=['title', 'author', 'date', 'time']

# System settings

# git working directory
# (clones will be placed here)
GIT_WD="/home/cem/website/git-wd"

# markdown file extension
MD_EXT=".md"


# Basic per repo workflow
# -----------------------
#
# 1) check if repo already cloned
#
# 2) if not clone it
#
# 3) else pull --> pull is done on branches, do below, after 5)
#
# 4) for every branch in DEF_BRANCHES
#
# 5) check-out
#
# 6) process

import os

from git_functions import git_cmd
from common import read_tb_and_content


#WD=os.getcwd()
#print(WD)
# (the CWD seems to be the directory from where pds.py is called)

# Menu generation workflow
# ------------------------
#
# The goal would be to generate the menus only once and reuse it
# for the different pages.
#
# The idea to accomplish this would be to use a class for menus.
# An instance should be created on global level, but nothing
# should be generated at this point, since we first need to refresh
# all the repos. (Therefor not using __init__.)
# The class should provide a method to 'get' the respective menu.
# This method should return the menu, creating it if it doesn't
# exist yet.

def preprocess_page(page_body):

    # workflow
    # -



def process_page(repo_name, branch, subdir, filename_md):

    # workflow
    # - read title block and content
    # - pre-process content
    # - process content through pandoc
    # - post-process content
    # - generate menus    
    # - put together
    # - write out --> needs to be in process_dir_recurse cause we
    #                 need to know if shall be the "index" page
    filepath_md=os.path.join(GIT_WD, repo_name, subdir, filename_md)
    page_body, title_block=read_tb_and_content(filepath_md, TB_LINES)

    print("TB: ", title_block)
    print("CONTENT: ", page_body)

    page_body_subst, plugin_blocks=preprocess_page(page_body)



def process_dir_recurse(repo_name, branch, subdir=""):
    dir=os.path.join(GIT_WD, repo_name)

    # workflow
    #
    # process content of this directory
    # - generate menus
    # - for every markdown file
    #     process page
    #       write out

    # (get directory content)
    dir_content_list=os.listdir(dir)

    for file in dir_content_list:
        if file.endswith(MD_EXT):
            process_page(repo_name, branch, subdir, file)




def checkout_all_repos(branch):

    # (get the cloned repos)
    repos_list=os.listdir(GIT_WD)

    has_branch_repo_list=[]

    oldwd=os.getcwd()
    for repo in repos_list:
        os.chdir( os.path.join(GIT_WD, repo) )
        # (checkout)
        # --> evtl. make this nicer e.g. check if branch exists
        ret=git_cmd("checkout", [ branch ])
        if ret == 0:
            # (add to return list)
            has_branch_repo_list.append(repo)
        else:
            print("pds: repo <repo_name> has no branch <branch>")
            continue

        # (update the branch)
        # --> evtl. also make this nicer e.g. check if up-to-date
        git_cmd("pull")

    os.chdir(oldwd)

    return has_branch_repo_list


def clone_all_repos():

    # (get the bare repos)
    bare_repos_list=os.listdir(REPO_DIR)

    # (check for base-layout)
    if not "base-layout.git" in bare_repos_list:
        print("pds: base-layout.git repo not found, aborting.")
        exit()

    # (check if already cloned)
    cloned_repos_list=os.listdir(GIT_WD)

    oldwd=os.getcwd()
    for bare_repo in bare_repos_list:
        repo_name=os.path.splitext(bare_repo)[0]

        if repo_name in cloned_repos_list:
            print("pds: repo <repo_name> already cloned, continuing...")
            continue

        # (clone)
        os.chdir(GIT_WD)
        git_cmd("clone", [ os.path.join(REPO_DIR, repo_barename) ])

    os.chdir(oldwd)


def main(branches=DEF_BRANCHES):

    # we need to clone and checkout _all_ repos before processing the content,
    # this is needed for the menu creation
    # (clone all repos)
    clone_all_repos()

    # (branch wise checkout and process)
    for branch in branches:

        has_branch_repo_list=checkout_all_repos(branch)

        # all the repos are ready, providing a directory structure to process
        for repo in has_branch_repo_list:
            print("repo: ", repo)
            process_dir_recurse(repo, branch)

            continue




main([ "public" ])

#process_repo("base-layout.git")

'''update given repo'''
# (check if repo exists)

'''update all repos'''



# commands to initialize a directory
#
# git init
# git clone --bare <repo> REPO_DIR/<repo>.git
# (set push destination)
# git remote add origin REPO_DIR/<repo>.git
#
# (enable/insert git hook to trigger pds update)
#
# manual:
# git push -u origin master
