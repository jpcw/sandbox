#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Generic tools
"""

__docformat__ = 'restructuredtext en'

import fnmatch
import os

from ConfigParser import SafeConfigParser
from exceptions import Exception


def recursive_glob(tree_root, pattern="*"):
    """Returns list of files matching pattern from tree_root."""

    if not os.path.isdir(tree_root):
        raise Exception("%s is not a directory" % tree_root)

    found_files = []
    for base, dirs, files in os.walk(tree_root):
        match_files = fnmatch.filter(files, pattern)
        found_files.extend(os.path.join(base, filename)
                           for filename in match_files)
    return found_files


def get_lines_from_file(filename):
    """Returns list of lines."""

    if not os.path.isfile(filename):
        raise Exception("%s is not a file" % filename)

    with open(filename, 'r') as myfile:
        return myfile.read().splitlines()


def write_lines_to_file(filename, text, mode='w'):
    """Writes text to file.

    if isinstance(text, list) text content is joined with'\n'.
    """
    if mode not in ['w', 'a']:
        raise Exception("%s not a correct mode ['a', 'w']" % mode)

    with open(filename, mode) as myfile:
        if isinstance(text, list):
            text = '\n'.join(text)
        return myfile.writelines(text)


def get_section_config(filename, section, ret_as_dict=True):
    """Returns section configuration, as dict if asked."""

    if not os.path.isfile(filename):
        raise Exception("%s is not a file" % filename)

    parser = SafeConfigParser()
    parser.read(filename)

    if not section in parser.sections():
        raise Exception("%s not found in %s" % (section, filename))

    if ret_as_dict:
        return dict(parser.items(section))

    return parser.items(section)


# vim:set et sts=4 ts=4 tw=80:
