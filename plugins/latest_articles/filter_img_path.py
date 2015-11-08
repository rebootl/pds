#!/usr/bin/python
'''Pandoc filter to insert path placeholder for images.'''

from pandocfilters import toJSONFilter, Para, Image

PATH_HASH = "PATH_178164f81917b8e87073295a635588de"

def repl_path(key, value, format, meta):
    if key == 'Image':
        alt, [ src, tit ] = value
        return Image( alt, [ PATH_HASH+src, tit ] )

if __name__ == "__main__":
    toJSONFilter(repl_path)
