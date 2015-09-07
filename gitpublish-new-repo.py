#!/usr/bin/python
#
# helper to create a bare repository on the remote server
#
# is called on the server itself
#
# sys.argv[1] repo name

import sys
import os

import config

from common import git_cmd, write_out

# settings

PDS_EXPATH = "/home/cem/Scripts/pds2/pds.py"

# processing
def new_repo(repo_name_in):

    repo_name = repo_name_in + ".git"
    repo_path = os.path.join(config.REPO_DIR, repo_name)

    git_opts = [ "--bare", repo_path ]
    git_cmd( "init", git_opts )

    # create hooks
    print("generating hooks:")

    hooks = [ 'post-receive', 'update' ]
    hooks_desc = [ 'initiate pds update, after a push',
                   'cleanup the git-wd, when a branch was deleted' ]
    hooks_content = [ '''#!/usr/bin/bash
#
# pds hook
# - initiate pds update, after a push
#
# hooks/post-receive
unset GIT_DIR
{}
'''.format(PDS_EXPATH),

'''#!/usr/bin/bash
#
# pds hook
# - cleanup the git-wd, when a branch was deleted
#
# hooks/update
# based on hooks/update.sample

# --- Command line
refname="$1"
oldrev="$2"
newrev="$3"

# --- Check types
# if $newrev is 0000...0000, it's a commit to delete a ref.
zero="0000000000000000000000000000000000000000"
if [ "$newrev" != "$zero" ]; then
    exit 0
fi

REPO_NAME_EXT=$(basename "$PWD")
REPO_NAME="${{REPO_NAME_EXT%.*}}"
echo "hook-update: a branch was deleted on $REPO_NAME"

GIT_WD="{}"

CLEANUP="$GIT_WD/$REPO_NAME"
echo "hook-update: removing git-wd: $CLEANUP"
rm -rf "$CLEANUP"
'''.format(config.GIT_WD) ]

    for i, hook in enumerate(hooks):
        print("- hooks/{} ({})".format(hook, hooks_desc[i]))
        # write hook
        hook_path = os.path.join(repo_path, "hooks", hook)

        write_out(hooks_content[i], hook_path)

        # make executable
        os.chmod(hook_path, 0o755)

    print("\nuse: git remote add <name> <url>")
    print("to add it to your local repo")


if len(sys.argv) < 2:
    print("usage: {} <repo-name>")
    print(".git is added to the repo name")
    sys.exit(1)
else:
    new_repo(sys.argv[1])
