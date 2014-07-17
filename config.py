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
REPO_DIR="/home/cem/website/repos"

# the name of the base repo
BASE_REPO_NAME="base-layout"

# the publish directory
PUBLISH_DIR="/home/cem/website/http-serv"

# Pandoc title block lines
TB_LINES=['title', 'author', 'date']
#TB_LINES=['title', 'author', 'date', 'time']

# Pandoc HTML template
HTML_TEMPLATE="/home/cem/website/templates/html5.html"

# exclude directories from processing
EXCLUDE_DIRS=[ ".git" ]

# exclude markdown files containing these keywords in 
# their name from the menus
# (e.g. useful for footer content like impressum, legal 
# notes or maybe in the future "posts" meaning single md 
# files whose content will be integrated in other pages)
MENU_EXCLUDE_FILES_MD=[ "impressum" ]

# Pandoc HTML type
# (==> default to html5)
#HTML_TYPE="html5"

# Pandoc table of content depth
# (==> think not used atm)
#TOC_DEPTH='5'

# Pandoc use div's to delimit sections
SECTION_DIV=True

# System settings
# ---------------

# git working directory
# (clones will be placed here)
GIT_WD="/home/cem/website/git-wd"

# markdown file extension
MD_EXT=".md"
