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
# 3) else pull --> pull is done on branches, below
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

def process_branch(repo_name, branch):
    os.chdir( os.path.join(GIT_WD, repo_name) )
    # (checkout the defined branch)
    # --> evtl. make this nicer e.g. check in process_repo first
    ret=git_cmd("checkout", [ branch ])
    if ret > 0:
        print("Branch not found, returning.")
        return

    # (update the branch)
    # --> evtl. also make this nicer e.g. check if up-to-date
    git_cmd("pull")

    # (process content)



def process_repo(repo_barename):
    repo_name=os.path.splitext(repo_barename)[0]

    oldcwd=os.getcwd()

#    print(repo_name)

    # (get the cloned repos)
    cloned_repos_list=os.listdir(GIT_WD)

#    print(cloned_repos_list)

    # (if the repo is not cloned yet, clone it)
    if not repo_name in cloned_repos_list:
        os.chdir(GIT_WD)
        git_cmd("clone", [ os.path.join(REPO_DIR, repo_barename) ])

    for branch in DEF_BRANCHES:
    # --> evtl. make DEF_BRANCHES a default argument
        process_branch(repo_name, branch)



process_repo("base-layout.git")

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
