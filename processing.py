#!/usr/bin/python
#
#
#

import os

import config

from common import write_out, copy_file
from page import Page


def process_dir_recurse(repo_name, branch, subpath=""):

    dir = os.path.join(config.GIT_WD, repo_name, subpath)

    # get directory content
    dir_content_list = os.listdir(dir)

    # filter dir content
    md_files_list = []
    subdirs_list = []
    other_files = []
    for file in dir_content_list:
        if file.endswith(config.MD_EXT):
            md_files_list.append(file)

        elif os.path.isdir(os.path.join(dir, file)):
            subdirs_list.append(file)

        # more filters might be specified here
        # ...

        else:
            other_files.append(file)

        # if no md file found, return (?)

    # remove excluded dirs
    # (debug print)
    #print("SUBDIRS LIST: ", subdirs_list)
    for excl_dir in config.EXCLUDE_DIRS:
        if excl_dir in subdirs_list:
            subdirs_list.remove(excl_dir)

    # set out dir
    if repo_name == config.BASE_REPO_NAME:
        out_dir=os.path.join(config.PUBLISH_DIR, branch, subpath)
    else:
        out_dir=os.path.join(config.PUBLISH_DIR, branch, repo_name, subpath)

    # process dir content
    # (markdown files)
    for idx, filename_md in enumerate(sorted(md_files_list)):

        # generate instance
        page_inst = Page(repo_name, branch, subpath, filename_md, idx)

        # set out filename
        if idx == 0:
            out_filename = "index.html"
        else:
            out_filename = os.path.splitext(filename_md)[0]+".html"

        # set out path
        out_filepath = os.path.join(out_dir, out_filename)

        # write out
        write_out(page_inst.page_html, out_filepath)

    # copy remaining files
    for file in other_files:
        in_filepath = os.path.join(dir, file)
        copy_file(in_filepath, out_dir)

    # recurse
    for subdir in subdirs_list:
        # the subdir needs to be:
        subpath_new=os.path.join(subpath, subdir)
    
        process_dir_recurse(repo_name, branch, subpath_new)
