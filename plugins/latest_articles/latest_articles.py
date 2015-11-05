'''latest articles preview'''

from datetime import datetime

NUM_OF_ARTICLES = 3

NUM_OF_PREVIEW_LINES = 10

DATE_FORMAT = "%Y-%m-%d"

def read_date(date_str):
    try:
        dt = datetime.strptime(date, date_format)
    except ValueError:
        dt = "BADDATE"


def latest_articles(branch):

    # get all pages
    pages = []
    for repo in branch.repos:
        for subpath in repo.subpaths:
            for page in subpath.pages:
                pages.append(page)

    # sort after date
    pages.sort(key=lambda k: k.date)


    for page in pages:
        print("PAGE DATE" , page.date, "PAGE NAME", page.out_filepath)


    return "", ""
