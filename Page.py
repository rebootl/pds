'''base page object'''

import os
import config

from common import read_tb_and_content, pandoc_pipe, write_out
from plugin_handler import get_cdata, plugin_cdata_handler, back_substitute
from nav_prim import gen_nav_primary
from nav_dir import gen_nav_pagelist, gen_nav_dirlist, gen_nav_path

class Page:

    def __init__(self, branch, repo, subpath, file_md):
        self.branch = branch
        self.repo = repo
        self.subpath = subpath
        self.file_md = file_md

        # markdown (input) filepath
        self.filepath_md = file_md.filepath

        # set out dir
        if self.repo.name == config.BASE_REPO_NAME:
            self.out_dir = os.path.join( config.PUBLISH_DIR,
                                         self.branch.out_name,
                                         self.subpath.path )
        else:
            self.out_dir = os.path.join( config.PUBLISH_DIR,
                                         self.branch.out_name,
                                         self.repo.name,
                                         self.subpath.path )
        # out filename
        if file_md.num == 0:
            self.out_filename = "index.html"
        else:
            self.out_filename = os.path.splitext(self.file_md.name)[0]+".html"
        # out path
        self.out_filepath = os.path.join(self.out_dir, self.out_filename)

        # navigation
        #self.nav_path = self.subpath.nav_path
        #self.nav_dirlist = self.subpath.nav_dirlist

        # load markdown and title block
        self.tb_values, \
        self.page_body_md = read_tb_and_content(self.filepath_md, 
                                             config.TB_LINES)
        self.meta_title = self.tb_values[0]
        self.meta_author = self.tb_values[1]
        self.meta_date = self.tb_values[2]

    def process(self):

        # substitute and process plugin content
        # sets:
        # - self.page_body_subst
        # - self.cdata_blocks
        # - self.plugin_blocks
        # - self.plugin_blocks_pdf
        # - self.plugin_pandoc_opts
        self.process_plugin_content()

        # primary navigation
        self.nav_primary = gen_nav_primary( self.branch.out_name,
                                            self.file_md.filepath )

        # page list
        self.nav_pagelist = gen_nav_pagelist( self.branch.out_name,
                                              self.repo.name,
                                              self.subpath.path,
                                              self.file_md.filepath )

        # add path and directory list (not on base repo)
#        if self.repo_name != config.BASE_REPO_NAME:
#            self.nav_path = gen_nav_path( self.branch_name,
#                                          self.repo_name,
#                                          self.subpath,
#                                          self.filepath_md )
#            self.nav_dirlist = gen_nav_dirlist( self.branch_name,
#                                                self.repo_name,
#                                                self.subpath,
#                                                self.filepath_md )

        # prepare pandoc opts
        self.prepare_pandoc()

        # process through pandoc
        self.page_html_subst = pandoc_pipe(self.page_body_subst,
                                           self.pandoc_opts)

        # back-substitute plugin content
        if self.plugin_blocks != []:
#            print("Plugin Blocks: ", self.plugin_blocks)
            self.page_html = back_substitute(self.page_html_subst,
                                             self.plugin_blocks)
        else:
            self.page_html = self.page_html_subst

    def process_plugin_content(self):
        # plugin substitution
        self.page_body_subst, \
        self.cdata_blocks = get_cdata(self.page_body_md)

        # process the plug-in content
        if self.cdata_blocks != []:
            self.plugin_blocks, \
            self.plugin_blocks_pdf, \
            self.plugin_pandoc_opts = plugin_cdata_handler(self.branch,
                                                             self.subpath,
                                                             self.cdata_blocks)
        else:
            self.plugin_blocks = []
            self.plugin_blocks_pdf = []
            self.plugin_pandoc_opts = []

    def prepare_pandoc(self):
        '''Collect the Pandoc options.'''
        self.pandoc_opts = []

        # set plugin opts
        for opt in self.plugin_pandoc_opts:
            self.pandoc_opts.append(opt)

        # set the out format
        self.pandoc_opts.append('--to=html5')

        # set the template
        self.pandoc_opts.append('--template='+config.HTML_TEMPLATE)

        # include the current branch
        # (the check is probably not needed, pandoc may do this as well)
        if self.branch.out_name != "":
            self.pandoc_opts.append('--variable=branch:'+self.branch.name)

        # set the title block opts
        for index, tb_value in enumerate(self.tb_values):
            self.pandoc_opts.append('--variable='+config.TB_LINES[index]+':'+tb_value)

        # don't put title on first base layout pages
        if self.repo.name == config.BASE_REPO_NAME and self.file_md.num == 0:
            self.pandoc_opts.append('--variable=title:')

        # include a table of content
        self.pandoc_opts.append('--toc')
        self.pandoc_opts.append('--toc-depth='+config.TOC_DEPTH)

        # use div's to delimit sections (optional)
        if config.SECTION_DIV:
            self.pandoc_opts.append('--section-divs')

        # include navigation
        self.pandoc_opts.append('--variable=nav-primary:'+self.nav_primary)

        # add page list
        if self.nav_pagelist != "":
            self.pandoc_opts.append('--variable=nav-pagelist:'+self.nav_pagelist)

        # add path / directory lists (not on main page)
        if self.subpath.nav_path != "":
            self.pandoc_opts.append('--variable=nav-path:'+self.subpath.nav_path)
        if self.subpath.nav_dirlist != "":
            self.pandoc_opts.append('--variable=nav-dirlist:'+self.subpath.nav_dirlist)

        # ... add more opts here ...

    def write_out(self):
#        print("Page: ", self.meta_title, self.out_filepath)
        write_out(self.page_html, self.out_filepath)
