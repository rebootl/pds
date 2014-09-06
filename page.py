

import os

import config

from common import read_tb_and_content, pandoc_pipe, gen_fortune, write_out, read_file
from plugin_handler import get_cdata, plugin_cdata_handler, back_substitute
#from menu import generate_base_menu, generate_repos_menu
from nav import primary_nav, secondary_nav

class Page:
    '''Page, processing.

Retrieve output:
HTML    <inst>.page_html
'''

    # (instance counter)
    inst_count=0

    fortune_msg="fortune mesg"


    def __init__(self, repo_name, branch, subpath, filename_md, new_fortune=False):
        self.repo_name=repo_name
        self.branch=branch
        self.subpath=subpath
        self.filename_md=filename_md

        self.new_fortune=new_fortune

        # (construct md filepath)
        self.filepath_md=os.path.join(config.GIT_WD, self.repo_name, self.subpath, self.filename_md)

        # (call process right away)
        self.process()

        Page.inst_count+=1


    def process(self):

        # (read markdown and title block)
        self.page_body_md, self.tb_values=read_tb_and_content(self.filepath_md, config.TB_LINES)

        # (substitute and process plugin content)
        self.process_plugin_content()

        # (generate menus)
        #self.base_menu=generate_base_menu(self.branch, self.filepath_md)
        #self.repos_menu=generate_repos_menu(self.branch, self.filepath_md)

        self.primary_nav=primary_nav(self.branch, self.filepath_md)
        self.secondary_nav=secondary_nav(self.branch, self.repo_name, self.filepath_md)

        # (set fortune message)
        if self.inst_count == 0:
            self.set_fortune()

        # (prepare pandoc opts)
        self.prepare_pandoc()

        # (process through pandoc)
        self.page_html_subst=pandoc_pipe(self.page_body_subst, self.pandoc_opts)

        # (back-substitute plugin content)
        if self.plugin_blocks != []:
            self.page_html=back_substitute(self.page_html_subst, self.plugin_blocks)
        else:
            self.page_html=self.page_html_subst


    def set_fortune(self):

        if config.MAKE_FORTUNE:
            if self.new_fortune:
                Page.fortune_msg=gen_fortune()
                # (store it)
                filepath=os.path.join(config.STORE_WD, "fortune_msg")
                write_out(Page.fortune_msg, filepath)
            else:
                filepath=os.path.join(config.STORE_WD, "fortune_msg")
                if os.path.isfile(filepath):
                    Page.fortune_msg=read_file(filepath)
                else:
                    print("Warning: No fortune message present yet.")
        else:
            Page.fortune_msg=""


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
        self.page_body_subst, self.cdata_blocks=get_cdata(self.page_body_md)

        # process the plug-in content
        if self.cdata_blocks != []:
            # --> self.subpath correct ?
            #print("self.subpath: ", self.subpath)
            self.plugin_blocks, self.plugin_blocks_pdf = plugin_cdata_handler(self.branch, self.subpath, self.cdata_blocks)

        else:
            self.plugin_blocks=[]
            self.plugin_blocks_pdf = []


    def prepare_pandoc(self):
        '''Collect the Pandoc options.'''

        self.pandoc_opts=[]

        # set the out format
        self.pandoc_opts.append('--to=html5')

        # set the template
        self.pandoc_opts.append('--template='+config.HTML_TEMPLATE)

        # include the current branch
        self.pandoc_opts.append('--variable=branch:'+self.branch)

        # set the title block opts
        for index, tb_value in enumerate(self.tb_values):
            self.pandoc_opts.append('--variable='+config.TB_LINES[index]+':'+tb_value)

        # include a table of content
        self.pandoc_opts.append('--toc')
        self.pandoc_opts.append('--toc-depth='+config.TOC_DEPTH)

        # use div's to delimit sections (optional)
        if config.SECTION_DIV:
            self.pandoc_opts.append('--section-divs')

        # include menus
        #self.pandoc_opts.append('--variable=base-menu:'+self.base_menu)
        #self.pandoc_opts.append('--variable=repos-menu:'+self.repos_menu)
        self.pandoc_opts.append('--variable=primary-nav:'+self.primary_nav)
        self.pandoc_opts.append('--variable=secondary-nav:'+self.secondary_nav)

        # include fortune message
        if config.MAKE_FORTUNE:
            self.pandoc_opts.append('--variable=fortune:'+self.fortune_msg)

        # .. more opts here ..
        
