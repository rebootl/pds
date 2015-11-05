'''plugin handling functions'''

import re

import config

from plugins.insert_file.insert_file import insert_file
from plugins.gallery.gallery import gallery
from plugins.tree.tree import tree
from plugins.metapost.metapost import metapost, metapost_ext
from plugins.repo_list.repo_list import repo_list
from plugins.latest_articles.latest_articles import latest_articles

# Settings
# --> Pandoc adds newlines into the div now...
# (My way of substitution is simple but it seems also fragile...)
# ==> adding newlines here to fix it, quick but still ugly...
# --> maybe use some sort of python temporary filename
PLUGIN_PLACEHOLDER = '<div id="placeholder">\n<p>\nSomething\n</p>\n</div>'
#PLUGIN_PLACEHOLDER='d8a2cabb38c68700bdef0112a5f2a35e'

def plugin_cdata_handler(branch, subdir, cdata_blocks):
    '''Receive the cdata blocks and forward them to the appropriate plugin.'''
    plugin_blocks = []
    plugin_blocks_pdf = []
    plugin_pandoc_opts = []

    for block in cdata_blocks:
        pandoc_opts = []
        # extract plugin name and content from cdata block
        block_split = block.split(']')
        plugin_name = block_split[0].strip('[[').strip()

        plugin_in = block_split[1].strip().strip('[').strip()

        # here now we forward the blocks to the appropriate plugins
        # Each plugin needs an entry here !

        if plugin_name == 'INSERTFILE':
            plugin_out, pdf_out = insert_file(subdir, plugin_in)

        elif plugin_name == 'GALLERY':
            plugin_out, pdf_out = gallery(subdir, plugin_in)

        elif plugin_name == 'TREE':
            plugin_out, pdf_out = tree(subdir, plugin_in)

        elif plugin_name == 'FIG':
            plugin_out, pdf_out = metapost(subdir, plugin_in)

        elif plugin_name == 'FIG_EXT':
            plugin_out, pdf_out = metapost_ext(subdir, plugin_in)

        elif plugin_name == 'REPO_LIST':
            plugin_out, pdf_out, pandoc_opts = repo_list(branch)

        elif plugin_name == 'LATEST_ARTICLES':
            plugin_out, pdf_out = latest_articles(branch)

        #elif plugin_name=' ... ':
        #	plugin_out, pdf_out = plugins. .. (plugin_content)

        # if no plugin is found return the raw content
        else:
            print("No plugin named:", plugin_name, "found,\n returning raw content.")
            plugin_out = block
            pdf_out = block

        plugin_blocks.append(plugin_out)
        plugin_blocks_pdf.append(pdf_out)
        plugin_pandoc_opts.extend(pandoc_opts)

    # (debug-print)
    #print("plugin blocks pdf plugin_handler: ", plugin_blocks_pdf)

    return plugin_blocks, plugin_blocks_pdf, plugin_pandoc_opts


def get_cdata(text):
    '''Get the cdata blocks and replace them by a placeholder.

Return the text and the blocks.'''
    #
    # the regex for cdata
    # should be <![TYPE[DATA]]> ==> changed to [[ TYPE ] [ DATA ]]
    re_cdata=re.compile(r'\[\[.+?\]\]', re.DOTALL)
    cdata_blocks=re_cdata.findall(text)

    text_rep=text
    for block in cdata_blocks:
        text_rep=text_rep.replace(block, PLUGIN_PLACEHOLDER)

    # (debug-info)
    #print('Cdata blocks:', cdata_blocks)
    #print('Text rep:', text_rep)

    return text_rep, cdata_blocks


def back_substitute(text, cdata_blocks):
    '''Back substitution of plugin content.'''
    for block in cdata_blocks:
        # (debug-info)
        #print('Block:', block)
        text=text.replace(PLUGIN_PLACEHOLDER, block, 1)

    # (debug-info)
    #print('Text:', text)

    return text
