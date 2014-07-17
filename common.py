



import os
import subprocess

import config


def git_cmd(action, opts=[]):
    '''execute git action'''
    git_cmd=[ "git", action ]+opts

    exitcode=subprocess.call(git_cmd)

    return exitcode


def read_tb_and_content(filepath_md, tb_lines):
    '''read out title block and content from a markdown file'''

    # open and read file lines
    with open(filepath_md, 'r') as f_op:
        file_lines=f_op.readlines()

    # succesively get the values and remove the lines
    title_block=[]
    for tb_line in tb_lines:
        full_line=file_lines[0]
        if full_line.startswith('%'):
            text=' '.join(full_line.split(' ')[1:]).rstrip()
            title_block.append(text)
            del file_lines[0]

    # join the lines
    file_body=''.join(file_lines)

    return file_body, title_block


def read_tb_lines(filepath_md, line_numbers=[0]):

    tb_lines=[]
    with open(filepath_md, 'r') as f_op:
        for line_num in line_numbers:
            tb_lines.append(f_op.readlines()[line_num])

    values=[]
    for tb_line in tb_lines:
        if tb_line.startswith('%'):
            text=' '.join(tb_line.split(' ')[1:]).rstrip()
            values.append(text)

    return values


def pandoc_pipe(content, opts):
    '''Create a pandoc pipe reading from a variable and returning the output.'''
    #
    # the pandoc command
    pandoc_command=['pandoc']
    # adding math support
    # (done by own functions)
    #opts.append('--gladtex')
    args=pandoc_command+opts
    # the pipe
    proc=subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    input=content.encode()
    output=proc.communicate(input=input)

    output=output[0].decode('utf-8')
    return output


def write_out(content, outfile):
    '''Write out content to file.'''
    out_dir=os.path.dirname(outfile)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    with open(outfile, 'w') as outfile_o:
        outfile_o.write(content)


def copy_file(in_path, out_dir):
    '''Call copy w/o preset directories.
(Not recursive.)
--> shutil.copy could be used for this.'''
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # using cp -u
    cp_command=['cp', '-u', in_path, out_dir]

    exitcode=subprocess.call(cp_command)
    #proc=subprocess.Popen(cp_command)