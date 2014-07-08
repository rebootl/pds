



#import os




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
