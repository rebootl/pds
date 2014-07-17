#!/usr/bin/python
#
#
#

import os

import config

from common import git_cmd


def checkout_all_repos(branch):

    # (get the cloned repos)
    repos_list=os.listdir(config.GIT_WD)

    has_branch_repo_list=[]

    oldwd=os.getcwd()
    for repo in repos_list:
        os.chdir( os.path.join(config.GIT_WD, repo) )
        # (checkout)
        # --> evtl. make this nicer e.g. check if branch exists
        ret=git_cmd("checkout", [ branch ])
        if ret == 0:
            # (add to return list)
            has_branch_repo_list.append(repo)
        else:
            print('pds: repo "{}" has no branch "{}"'.format(repo, branch))
            continue

        # (update the branch)
        # --> evtl. also make this nicer e.g. check if up-to-date
        git_cmd("pull")

    os.chdir(oldwd)

    return has_branch_repo_list


def clone_all_repos():

    # (get the bare repos)
    bare_repos_list=os.listdir(config.REPO_DIR)

    # (check for base-layout)
    if not config.BASE_REPO_NAME+".git" in bare_repos_list:
        print('pds: {}.git repo not found, aborting.'.format(config.BASE_REPO_NAME))
        exit()

    # (check if already cloned)
    cloned_repos_list=os.listdir(config.GIT_WD)

    oldwd=os.getcwd()
    for bare_repo in bare_repos_list:
        repo_name=os.path.splitext(bare_repo)[0]

        if repo_name in cloned_repos_list:
            print('pds: repo "{}" already cloned, continuing...'.format(repo_name))
            continue

        # (clone)
        os.chdir(config.GIT_WD)
        git_cmd("clone", [ os.path.join(config.REPO_DIR, bare_repo) ])

    os.chdir(oldwd)