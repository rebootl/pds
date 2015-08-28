'''common functions'''

import os
import subprocess
import textwrap

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
            try:
                tb_lines.append(f_op.readlines()[line_num])
            except IndexError:
                pass

    values=[]
    for tb_line in tb_lines:
        if tb_line.startswith('%'):
            text=' '.join(tb_line.split(' ')[1:]).rstrip()
            values.append(text)

    return values


def get_title(filepath_md):
    '''Get the page title as link text, returning the filename as fallback[^1].

[^1]: currently this is commented, why ?
'''

    tb_title_list = read_tb_lines(filepath_md, [0])
    if tb_title_list == []:
        # (use the filename w/o extension as fallback)
        #link_text=os.path.splitext(os.path.basename(filepath_md))[0]
        link_text = ""
    else:
        link_text = tb_title_list[0]

    return link_text


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


def read_file(filepath):

    if not os.path.isfile(filepath):
        print("Warning: file not found: ", filepath)
        return ""

    with open(filepath, 'r') as f:
        content=f.read()

    return content


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


def gen_fortune():
    '''Generate a fortune message.
Using fortune.'''
    # -s short
    fortune_cmd=['fortune', '-s']

    proc=subprocess.Popen(fortune_cmd, stdout=subprocess.PIPE)
    output=proc.communicate()[0]

    out_dec=output.decode('utf-8')

    # wrap the text
    out_wrap=textwrap.fill(out_dec, config.FORTUNE_WRAP_AT)

    return out_wrap


# (from new_simple_cms)
def copy_file_abs(inpath, out_dir):
    '''Call copy w/o preset directories.
(Not recursive.)
--> shutil.copy could be used for this.'''
    # using cp -u
    cp_command=['cp', '-u', inpath, out_dir]

    proc=subprocess.Popen(cp_command)


def get_dir_desc(dir_path_abs):
    '''get a repo/directory description text

if present use the description file
if not present use the title from the first markdown file
fallback to text
'''
    # try description file
    desc_filepath = os.path.join(dir_path_abs, config.REPO_DESC_FILENAME)

    if os.path.isfile(desc_filepath):
        with open(desc_filepath, 'r') as f:
            desc = f.read()
        return desc

    # try the first md file
    files = os.listdir(dir_path_abs)

    first_md_file = ""
    for file in sorted(files):
        if file.endswith(config.MD_EXT):
            first_md_file = file
            break

    if first_md_file == "":
        return "<pre>No description (markdown file) available, yet...</pre>"

    md_filepath_abs = os.path.join(dir_path_abs, first_md_file)

    desc = get_title(md_filepath_abs)

    if desc == "":
        return "<pre>No description (page title) available...</pre>"

    return desc
