'''pds git functions
'''

import os
import subprocess



def git_clone(opts):
    '''clone git repo'''
    pass



def git_cmd(action, opts=[]):
    '''execute git action'''
    git_cmd=[ "git", action ]+opts

    exitcode=subprocess.call(git_cmd)

    return exitcode







def git_call(dir, action, opts=[]):
    '''execute given git action inside given directory'''

    oldcwd=os.getcwd()
    os.chdir(dir)

    git_cmd=[ "git", action ]+opts

    subprocess.call(git_cmd)

    os.chdir(oldcwd)
