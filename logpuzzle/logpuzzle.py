#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def sort_by_name(filepath):
    match = re.search(r'-(\w+)-(\w+)\.\w+', filepath)
    if match:
        return match.group(2)
    else:
        return filepath


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
     extracting the hostname from the filename itself.
     Screens out duplicate urls and returns the urls sorted into
     increasing order."""
    under_score_index = filename.index('_')
    host_name = filename[under_score_index + 1:]
    urls = {}
    file = open(filename)
    for line in file:
        match = re.search(r'"GET (\S+)', line)
        if match:
            path = match.group(1)
            if 'puzzle' in path:
                host_name_path = 'http://' + host_name + path
                urls[host_name_path] = 1
    return sorted(urls.keys(), key=sort_by_name)


def download_images(urls, directory):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an _before.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    index = file(os.path.join(directory, 'index.html'), 'w')
    index.write('<html><body>\n')
    i = 0
    for url in urls:
        file_name = 'img%d' % i
        print 'downLoading...', url
        urllib.urlretrieve(url, os.path.join(directory, file_name))
        index.write('<img src="%s">' % (file_name,))
        i += 1
    index.write('\n</body></html>\n')
    index.close()


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)


if __name__ == '__main__':
    main()
