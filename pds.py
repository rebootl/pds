#!/usr/bin/python
'''a personal documentation system or...

...a git based static website generator'''
#
#
#
#

# improvements:
# - better plugin substitution
# -

import os

import config

from processing import process_dir_recurse
from git_processing import clone_all_repos, checkout_all_repos

# (test current working directory)
#WD=os.getcwd()
#print(WD)
# (the CWD seems to be the directory from where pds.py is called)

def main(branches=config.DEF_BRANCHES):

    # we need to clone and checkout _all_ repos before processing the content,
    # this is needed for the menu creation
    # (clone all repos)
    clone_all_repos()

    # (branch wise checkout and process)
    for branch in branches:

        has_branch_repo_list = checkout_all_repos(branch)

        # all the repos are ready, providing a directory structure to process
        for repo in has_branch_repo_list:
            print("repo: ", repo)
            process_dir_recurse(repo, branch)




main([ "public", "preview" ])



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
