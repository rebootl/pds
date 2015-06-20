#!/usr/bin/python
'''pds - settings file'''
#
#
#
#
# Per website settings
# --------------------

# the branches to process
DEF_BRANCHES=[ "public", "private", "preview" ]

# the repository path
REPO_DIR="/home/cem/website2/repos"

# the name of the base repo
BASE_REPO_NAME="base-layout"

# the publish directory
PUBLISH_DIR="/home/cem/website2/http-serv"

# Pandoc title block lines
TB_LINES=['title', 'author', 'date']
#TB_LINES=['title', 'author', 'date', 'time']

# Pandoc HTML template
HTML_TEMPLATE="/home/cem/website2/templates/html5.html"

# exclude directories from processing
EXCLUDE_DIRS=[ ".git" ]



# menu name for /index.html
#MENU_INDEX_NAME="Home"

# exclude markdown files containing these keywords in 
# their name from the menus
# (e.g. useful for footer content like impressum, legal 
# notes or maybe in the future "posts" meaning single md 
# files whose content will be integrated in other pages)
MENU_EXCLUDE_FILES_MD=[ "impressum" ]

# custom navigation: filename of an optional repo description file
REPO_DESC_FILENAME="repo.desc"

# Pandoc HTML type
# (==> default to html5)
#HTML_TYPE="html5"

# Pandoc table of content depth
# (--> think not used atm ==> is used)
TOC_DEPTH='5'

# Pandoc use div's to delimit sections
SECTION_DIV=True

# Generate a fortune message
MAKE_FORTUNE=True
# wrap the lines at n
FORTUNE_WRAP_AT=40



# System settings
# ---------------

# git working directory
# (clones will be placed here)
GIT_WD="/home/cem/website2/git-wd"

# markdown file extension
MD_EXT=".md"

# additional (persistent) working directory
# (currently used to store the fortune message)
STORE_WD="/home/cem/website2/store-wd"
