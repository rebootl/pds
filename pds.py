#!/usr/bin/python
'''a personal documentation system or...

...a git based static website generator'''
#
#
#
# improvements
# ------------
# - better plugin substitution
# - ..
#
#
# structure plan
# --------------
#
# branch
#    \
#    repo   --  --  subpath
#       \              |- pages
#       page           |- subdirs
#       page
#       subdir  --  subpath
#          \
#          page
#          page
#       subdir  --  subpath
#          \
#          page
#          page
#          page
#

import os

import config

from Branch import Branch
from git_processing import clone_all_repos

def main(branches=config.DEF_BRANCHES):

    # we need to clone and checkout _all_ repos before processing the content,
    # this is needed for the menu creation

    # clone all repos
    print("pds: cloning all repositories\n")
    clone_all_repos()

    # (branch wise checkout and process)
    print("\npds: branch wise checkout and process")
    for branch in branches:

        print("\npds: branch: *{}*\n".format(branch))

        # this initiates checkout of all repos
        # and loading of files and subdirectories
        branch_inst = Branch(branch)
        #       |
        #   self.checkout_all_repos()
        #     for every repo
        #       repo_inst
        #           |
        #         self.checkout()
        #         if has branch
        #           branch.repos.append(self)
        #         subpath
        #             |
        #           repo.subpaths.append(self)
        #           self.get_files()
        #           files_md
        #           files_others
        #           subdirs
        #              |
        #             subpath_inst
        #

        # all the repos are ready, providing a directory structure to process
#        print("pds: branch *{}* is ready on all repositories, continuing...".format(branch))

#        print("\npds: processing {}".format(branch))

#        for repo_inst in branch_inst.repos:

            #print("\nrepo:", repo)

            #repo_inst.get_files_recurse()
            #repo_inst.load_pages()
            #repo_inst.set_description()

            # (debug print)
            #for file in repo_inst.md_files:
            #    print(file.name, file.subpath)
            # (debug print)
            #for file in repo_inst.other_files:
            #    print(file.name, file.subpath)

#        for repo_inst in branch_inst.repos:

#            for page_inst in repo_inst.pages:

#                page_inst.process()
#                page_inst.write_out()

#            repo_inst.copy_files()

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
