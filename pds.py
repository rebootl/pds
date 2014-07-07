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


# System settings

# git working directory
# (clones will be placed here)
GIT_WD="/home/cem/website/git-wd"



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


#WD=os.getcwd()
#print(WD)
# (the CWD seems to be the directory from where pds.py is called)

def process_dir_recurse(repo_name, branch):
    dir=os.path.join(GIT_WD, repo_name)

    # workflow
    #
    # process content of this directory
    #
    # write out



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

    for bare_repo in bare_repos_list:
        repo_name=os.path.splitext(bare_repo)[0]

        if repo_name in cloned_repos_list:
            print("pds: repo <repo_name> already cloned, continuing...")
            continue

        # (clone)
        oldwd=os.getcwd()
        os.chdir(GIT_WD)
        git_cmd("clone", [ os.path.join(REPO_DIR, repo_barename) ])
        os.chdir(oldpwd)


def main(branches=DEF_BRANCHES):

    # we need to clone and checkout _all_ repos before processing the content,
    # this is needed for the menu creation
    clone_all_repos()

    # (checkout and process branch wise)
    for branch in branches:

        has_branch_repo_list=checkout_all_repos(branch)

        # all the repos are ready, providing a directory structure to process
        for repo in has_branch_repo_list:
            print("repo: ", repo)
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
