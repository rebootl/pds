#!/usr/bin/python
#
#
#

import os

import config

from menu import generate_base_menu, generate_repos_menu
from common import read_tb_and_content, pandoc_pipe, write_out, copy_file
from plugin_handler import get_cdata, plugin_cdata_handler, back_substitute


def prepare_pandoc(branch, tb_values, base_menu, repos_menu, fortune_msg):
    '''collect the options for the output'''

    pandoc_opts=[]

    # set the out format
    pandoc_opts.append('--to=html5')

    # set the template
    pandoc_opts.append('--template='+config.HTML_TEMPLATE)

    # include the current branch
    pandoc_opts.append('--variable=branch:'+branch)

    # set the title block opts
    for index, tb_value in enumerate(tb_values):
        pandoc_opts.append('--variable='+config.TB_LINES[index]+':'+tb_value)

    # include a table of content
    pandoc_opts.append('--toc')
    pandoc_opts.append('--toc-depth='+config.TOC_DEPTH)

    # use div's to delimit sections (optional)
    if config.SECTION_DIV:
        pandoc_opts.append('--section-divs')

    # include menus
    pandoc_opts.append('--variable=base-menu:'+base_menu)
    pandoc_opts.append('--variable=repos-menu:'+repos_menu)

    # --> include toc

    # include fortune message
    if config.MAKE_FORTUNE:
        pandoc_opts.append('--variable=fortune:'+fortune_msg)

    # .. more opts here ..

    return pandoc_opts


def process_plugin_content(page_body):

    # --> allow plugins to return pandoc variables

    # plugin substitution
    page_body_subst, cdata_blocks=get_cdata(page_body)

    # process the plug-in content
    if cdata_blocks != []:
        plugin_blocks, plugin_blocks_pdf = plugin_cdata_handler(subdir, cdata_blocks)

    else:
        plugin_blocks=[]
        plugin_blocks_pdf = []

    return page_body_subst, plugin_blocks, plugin_blocks_pdf


def process_page(repo_name, branch, subpath, filename_md, fortune_msg):

    # workflow
    # - read title block and content
    # - pre-process content (plugins and math)
    # - generate menus    
    # - put together
    # - process content (pandoc)
    # - post-process content
    # - write out --> needs to be in process_dir_recurse cause we
    #                 need to know if it shall be the "index" page
    filepath_md=os.path.join(config.GIT_WD, repo_name, subpath, filename_md)
    page_body_md, tb_vals=read_tb_and_content(filepath_md, config.TB_LINES)

    #print("TB: ", tb_vals)
    #print("CONTENT: ", page_body_md)

    # (plugin content)
    page_body_md_subst, plugin_blocks, plugin_blocks_pdf=process_plugin_content(page_body_md)
    # (math content)
    # --> here <--

    # (generate menus)
    base_menu=generate_base_menu(branch, filepath_md)
    repos_menu=generate_repos_menu(branch, filepath_md)
    # (evtl.)
    #pages_menu=[]

    # (put together)
    pandoc_opts=prepare_pandoc(branch, tb_vals, base_menu, repos_menu, fortune_msg)

    # (process through pandoc)
    page_html_subst=pandoc_pipe(page_body_md_subst, pandoc_opts)

    # (back-substitute)
    if plugin_blocks != []:
        page_html=back_substitute(page_html_subst, plugin_blocks)
    else:
        page_html=page_html_subst

    #print("HTML: ", page_html)

    return page_html


def process_dir_recurse(repo_name, branch, fortune_msg, subpath=""):
    dir=os.path.join(config.GIT_WD, repo_name, subpath)

    # workflow
    #
    # process content of this directory
    # - generate menus
    # - for every markdown file
    #     process page
    #     write out
    # copy remaining content
    # recurse into subdirs

    # (get directory content)
    dir_content_list=os.listdir(dir)

    # (filter dir content)
    md_files_list=[]
    subdirs_list=[]
    other_files=[]
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
    print("SUBDIRS LIST: ", subdirs_list)
    for excl_dir in config.EXCLUDE_DIRS:
        if excl_dir in subdirs_list:
            subdirs_list.remove(excl_dir)

    # (set out dir)
    if repo_name == config.BASE_REPO_NAME:
        out_dir=os.path.join(config.PUBLISH_DIR, branch, subpath)
    else:
        out_dir=os.path.join(config.PUBLISH_DIR, branch, repo_name, subpath)

    # process dir content
    # (markdown files)
    for idx, file_md in enumerate(sorted(md_files_list)):
        page_html=process_page(repo_name, branch, subpath, file_md, fortune_msg)

        # (set out filename)
        if idx == 0:
            out_filename="index.html"
        else:
            out_filename=os.path.splitext(file_md)[0]+".html"

        # (set out path)
        out_filepath=os.path.join(out_dir, out_filename)

        # (write out)
        write_out(page_html, out_filepath)

    # (copy remaining files)
    for file in other_files:
        in_filepath=os.path.join(dir, file)
        copy_file(in_filepath, out_dir)

    # (recurse)
    for subdir in subdirs_list:
        # the subdir needs to be:
        subpath_new=os.path.join(subpath, subdir)

        process_dir_recurse(repo_name, branch, fortune_msg, subpath_new)
