import os
import config

from common import read_tb_and_content, pandoc_pipe, write_out, read_file
from plugin_handler import get_cdata, plugin_cdata_handler, back_substitute
from nav_prim import gen_nav_primary
from nav_dir import gen_nav_pagelist, gen_nav_dirlist, gen_nav_path
from repo_list import gen_repo_list

class Page:
    '''Page, processing.

Retrieve output:
HTML    <inst>.page_html
'''

    # instance counter
    inst_count=0

    def __init__(self, branch, repo_name, subpath, filename_md, idx):
        self.repo_name = repo_name
        if branch == config.MAIN_BRANCH:
            self.branch = ""
        else:
            self.branch = branch
        self.subpath = subpath
        self.filename_md = filename_md
        self.idx = idx

        self.repo_list = ""
        self.nav_path = ""
        self.nav_dirlist = ""

        # construct md filepath
        self.filepath_md = os.path.join(config.GIT_WD, self.repo_name, self.subpath, self.filename_md)

        # call process right away
        self.process()

        Page.inst_count += 1

    def process(self):

        # read markdown and title block
        self.page_body_md, self.tb_values = read_tb_and_content(self.filepath_md, config.TB_LINES)

        # substitute and process plugin content
        self.process_plugin_content()

        # primary navigation
        self.nav_primary = gen_nav_primary(self.branch, self.filepath_md)

        # page list
        self.nav_pagelist = gen_nav_pagelist(self.branch, self.repo_name, self.subpath, self.filepath_md)

        # set repository list on main page
        if self.repo_name == config.BASE_REPO_NAME and self.idx == 0 and self.subpath == "":
            self.repo_list = gen_repo_list(self.branch)
            # (debug print)
            print("pds: (Placed repo list.)")

        # add path and directory list (not on main page)
        if self.repo_name != config.BASE_REPO_NAME:
            self.nav_path = gen_nav_path(self.branch, self.repo_name, self.subpath, self.filepath_md)
            self.nav_dirlist = gen_nav_dirlist(self.branch, self.repo_name, self.subpath, self.filepath_md)

        # prepare pandoc opts
        self.prepare_pandoc()

        # process through pandoc
        self.page_html_subst = pandoc_pipe(self.page_body_subst, self.pandoc_opts)

        # back-substitute plugin content
        if self.plugin_blocks != []:
            self.page_html = back_substitute(self.page_html_subst, self.plugin_blocks)
        else:
            self.page_html = self.page_html_subst

    def process_plugin_content(self):
        '''Process plugin content.
Sets:
- self.page_body_subst
- self.cdata_blocks
- self.plugin_blocks
- self.plugin_blocks_pdf
'''
        # --> allow plugins to return pandoc variables

        # plugin substitution
        self.page_body_subst, self.cdata_blocks = get_cdata(self.page_body_md)

        # process the plug-in content
        if self.cdata_blocks != []:
            # --> self.subpath correct ?
            #print("self.subpath: ", self.subpath)
            self.plugin_blocks, self.plugin_blocks_pdf = plugin_cdata_handler(self.branch, self.subpath, self.cdata_blocks)

        else:
            self.plugin_blocks = []
            self.plugin_blocks_pdf = []

    def prepare_pandoc(self):
        '''Collect the Pandoc options.'''

        self.pandoc_opts = []

        # set the out format
        self.pandoc_opts.append('--to=html5')

        # set the template
        self.pandoc_opts.append('--template='+config.HTML_TEMPLATE)

        # include the current branch
        # (the check is probably not needed, pandoc may do this as well)
        if self.branch != "":
            self.pandoc_opts.append('--variable=branch:'+self.branch)

        # set the title block opts
        for index, tb_value in enumerate(self.tb_values):
            self.pandoc_opts.append('--variable='+config.TB_LINES[index]+':'+tb_value)

        # don't put title on first base layout pages
        if self.repo_name == config.BASE_REPO_NAME and self.idx == 0:
            self.pandoc_opts.append('--variable=title:')

        # include a table of content
        self.pandoc_opts.append('--toc')
        self.pandoc_opts.append('--toc-depth='+config.TOC_DEPTH)

        # use div's to delimit sections (optional)
        if config.SECTION_DIV:
            self.pandoc_opts.append('--section-divs')

        # include navigation
        self.pandoc_opts.append('--variable=nav-primary:'+self.nav_primary)
#        self.pandoc_opts.append('--variable=secondary-nav:'+self.secondary_nav)
#        self.pandoc_opts.append('--variable=custom-nav:'+self.custom_nav)

        # set repository list on main page
        if self.repo_list != "":
            self.pandoc_opts.append('--variable=repo-list:'+self.repo_list)

        # add page list
        if self.nav_pagelist != "":
            self.pandoc_opts.append('--variable=nav-pagelist:'+self.nav_pagelist)

        # add path / directory lists (not on main page)
        if self.nav_path != "":
            self.pandoc_opts.append('--variable=nav-path:'+self.nav_path)
        if self.nav_dirlist != "":
            self.pandoc_opts.append('--variable=nav-dirlist:'+self.nav_dirlist)

        # ... add more opts here ...
