#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Doc here.
"""

__docformat__ = 'restructuredtext en'

import argparse
import fnmatch
import os
import sys

from ConfigParser import SafeConfigParser
from exceptions import Exception


def recursive_glob(tree_root, pattern="*"):
    """Returns list of files matching pattern from tree_root."""

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

    if isinstance(text, list) we join list content.
    """
    if mode not in ['w', 'a']:
        raise Exception("%s not a correct mode ['a', 'w']" % mode)

    with open(filename, mode) as myfile:
        if isinstance(text, list):
            text = '\n'.join(text)
        return myfile.writelines(text)


def search_and_replace_lines(search, replace, lines):
    """Search and replace."""

    return [line.replace(search, replace) for line in lines]


def extract_patterns(lines, sep):
    """Returns list of splited(sep) lines."""

    return (tuple(line.split(sep)) for line in lines)


def get_config(filename):
    """Returns configuration."""

    parser = SafeConfigParser()
    parser.read(filename)
    return dict(parser.items('options'))


def main(settings):
    """."""
    files = recursive_glob(settings['source_dir'], settings['filter'])
    patterns = extract_patterns(get_lines_from_file(settings['patterns']),
                                settings['sep'])

    for filename in files:
        lines = get_lines_from_file(filename)
        for search, replace in patterns:
            lines = search_and_replace_lines(search, replace, lines)

        write_lines_to_file(filename, lines)


if __name__ == '__main__':
    settings = {'patterns': None, 'filter': None, 'sep': None,
                'source_dir': None}
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default="config.cfg",
                        help="config filename, default : config.cfg")
    parser.add_argument('-p', '--patterns',
                        help="patterns file, overrides config file option")
    parser.add_argument('-f', '--filter',
                        help="pattern filter fname, overrides config option")
    parser.add_argument('-s', '--sep',
                        help="split separator, overrides config option")
    parser.add_argument('--source_dir',
                        help="source directory, overrides config option")
    args = parser.parse_args()

    if not os.path.isfile(args.config):
        sys.exit("%s not found" % args.config)

    cfg_options = get_config(args.config)
    settings.update(cfg_options)

    for key in settings:
        if getattr(args, key):
            settings[key] = getattr(args, key)

    if not os.path.isfile(settings['patterns']):
        sys.exit("%s not found" % settings['patterns'])

    if not all(settings.values()):
        sys.exit("%s missing sorry!" % [key for key in settings if
                                        not settings[key]])
    main(settings)

# vim:set et sts=4 ts=4 tw=80:
