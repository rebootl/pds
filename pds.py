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

from branch import Branch
#from repo import Repo
#from processing import process_dir_recurse
#from git_processing import clone_all_repos, checkout_all_repos
from git_processing import clone_all_repos

# (test current working directory)
#WD=os.getcwd()
#print(WD)
# (the CWD seems to be the directory from where pds.py is called)

def main(branches=config.DEF_BRANCHES):

    # we need to clone and checkout _all_ repos before processing the content,
    # this is needed for the menu creation

    # clone all repos
    print("pds: cloning all repositories")

    clone_all_repos()

    # (branch wise checkout and process)
    print("\npds: branch wise checkout and process")

    for branch in branches:

        print("\npds: branch: *{}*".format(branch))
        print("\npds: checkout and update".format(branch))

        branch_inst = Branch(branch)
        branch_inst.checkout_all_repos()

        # all the repos are ready, providing a directory structure to process
        print("pds: branch *{}* is ready on all repositories, continuing...".format(branch))

        print("\npds: processing {}".format(branch))

        for repo_inst in branch_inst.repos:

            #print("\nrepo:", repo)

            repo_inst.get_files_recurse()
            repo_inst.load_pages()

            # (debug print)
            #for file in repo_inst.md_files:
            #    print(file.name, file.subpath)
            # (debug print)
            #for file in repo_inst.other_files:
            #    print(file.name, file.subpath)

        for repo_inst in branch_inst.repos:

            for page_inst in repo_inst.pages:

                page_inst.process()
                page_inst.write_out()

            repo_inst.copy_files()

# [re1] ==> use Repo object
#            print('pds: repo: "{}"'.format(repo))
#            process_dir_recurse(repo, branch)


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
