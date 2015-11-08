'''pds - settings file'''

# General
# -------
# the publish directory
PUBLISH_DIR = "/home/cem/website2/http-serv"

# git working directory
# (clones will be placed here)
GIT_WD = "/home/cem/website2/git-wd"


# Branches
# --------
# the branches to process
DEF_BRANCHES = [ "public", "private", "preview" ]

# the main branch
# this branch is published directly in the publish directory,
# all other branches receive respective subdirectories
MAIN_BRANCH = "public"


# Repositories
# ------------
# path to the (bare) repositories
REPO_DIR = "/home/cem/website2/repos"

# the name of the base repo
# this repository is published directly in the publish directory,
# while all other receive respective subdirectories,
# so it is supposed to contain the homepage, css, evtl. logos etc.
BASE_REPO_NAME = "base-layout"


# Pages
# -----
# title block lines
# equivalent to Pandoc title block
# - one item per line (no multi-line items supported)
# - lines must start with a %
TB_LINES = ['title', 'author', 'date']

# date format (acc. to Python datetime.datetime.strptime)
DATE_FORMAT = "%Y-%m-%d"

# markdown file extension
MD_EXT = ".md"


# Excludes
# --------
# exclude directories from processing
EXCLUDE_DIRS = [ ".git", "localfont" ]

# exclude markdown files from the menus
# exclude markdown files containing these keywords in 
# their name from the menus
# (e.g. useful for footer content like impressum, legal notes)
#
# --> is this currently implemented ?
#
MENU_EXCLUDE_FILES_MD = [ "impressum" ]

# directory description file
#
# --> cleanup
#
DIR_DESC_FILENAME = "dir.shortdesc"
REPO_DESC_FILENAME = "dir.shortdesc"


# Pandoc
# ------
# Pandoc HTML template
HTML_TEMPLATE = "/home/cem/website2/templates/html5.html"

# Pandoc table of content depth
# (--> think not used atm ==> is used)
TOC_DEPTH = '5'

# Pandoc use div's to delimit sections
SECTION_DIV = True


# Internal
# --------
BADDATE_STR = "BAD DATE FORMAT"
