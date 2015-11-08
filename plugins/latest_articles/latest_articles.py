'''latest articles preview'''

import config

from common import pandoc_pipe

NUM_OF_ARTICLES = 5
NUM_OF_PREVIEW_LINES = 10

ARTICLE_PREVIEW_TEMPLATE = "/home/cem/Scripts/pds2/plugins/latest_articles/article-preview.html5"

# insert path placeholder for images using a pandoc filter
PANDOC_FILTER_IMG_PATH = "/home/cem/Scripts/pds2/plugins/latest_articles/filter_img_path.py"
PATH_HASH = "PATH_178164f81917b8e87073295a635588de"

def latest_articles(branch):

    # get all pages
    pages = []
    for repo in branch.repos:
        for subpath in repo.subpaths:
            for page in subpath.pages:
                if not page.date_obj == config.BADDATE_STR:
                    pages.append(page)

    # sort after date
    pages.sort(key=lambda k: k.date_obj.timestamp())
    pages.reverse()
    for page in pages:
        print("PAGE DATE" , page.date_obj, "PAGE NAME", page.out_filepath)    

    pandoc_opts = [ '--to=json',
                    '--template='+ARTICLE_PREVIEW_TEMPLATE,
                    '--filter='+PANDOC_FILTER_IMG_PATH ]
    latest_articles_html = ""
    for page in pages[:NUM_OF_ARTICLES]:
        lines = []
        for line in page.page_body_md.splitlines()[:NUM_OF_PREVIEW_LINES]:
            lines.append(line)
        body_part_md = '\n'.join(line for line in lines)

        print("BODY PART MD", body_part_md)

        for index, tb_value in enumerate(page.tb_values):
            pandoc_opts.append('--variable='+config.TB_LINES[index]+':'+tb_value)
        body_part_html = pandoc_pipe(body_part_md, pandoc_opts)

        print("BODY_PART_HTML", body_part_html)

        # replace the placeholder by the actual path...
        



    return "", ""
