#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/
import commands
import os
import re
import shutil
import sys

"""Copy Special exercise
"""


# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dirname):
    paths = os.listdir(dirname)
    list_of_Special_files = []
    for file in paths:
        match = re.search(r'__(\w+)__', file)
        if match:
            abs_file_name = os.path.abspath(os.path.join(dirname, file))
            list_of_Special_files.append(abs_file_name)
    return list_of_Special_files


def copy_files(file_names, to_dir):
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    for path in file_names:
        fname = os.path.basename(path)
        shutil.copy(path, os.path.join(to_dir, fname))


def zip_files(special_file_names, todir):
    cmd = 'zip -j ' + todir + ' ' + ' '.join(special_file_names)
    print "Executin I'm going to do:" + cmd
    (status, output) = commands.getstatusoutput(cmd)
    # If command had a problem (status is non-zero),
    # print its output to stderr and exit.
    if status:
        sys.stderr.write(output)
        sys.exit(1)


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print "error: must specify one or more dirs"
        sys.exit(1)

    # +++your code here+++
    # Call your functions

    for dirname in args:
        special_file_names = get_special_paths(dirname)
    if todir:
        copy_files(special_file_names, todir)
    elif tozip:
        zip_files(special_file_names, tozip)
    else:
        print '\n'.join(special_file_names)


# print list_of_special_files

if __name__ == "__main__":
    main()
