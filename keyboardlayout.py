#!/usr/bin/env python3

"""
Keyboard layout generator.

Usage:
    layout.py <rows> <columns> <keycodefile> <layoutfile> <command> [--filter=<tag>] [--reverse] [--checkkeycodes]
    layout.py (-h | --help)
    layout.py --version

Options:
    -h --help       Show this screen.
    --version       Show version.
    --reverse       Reverse the columns for all layers (useful for upside-down PCBs)
    --filter=<tag>  Include only layout sections matching <tag>

"""

#   Copyright 2016 Daniel P. Seemuth
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import collections
import sys


__version__ = '0.2.0'

__title__ = 'keyboardlayout'
__author__ = 'Daniel P. Seemuth'
__description__ = 'Keyboard layout generator for keyboards from uniquekeyboard.com'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Daniel P. Seemuth'


class KeyType:
    NORMAL = 0
    FN = 1
    SPACEFN = 2
    SWITCHLAYER = 3
    MEDIA = 4
    TOGGLEFN = 5


class Key:
    """One key's assignment: value and type.

    """

    def __init__(self, keyval, keytype=KeyType.NORMAL):
        self.keyval = keyval
        self.keytype = keytype


    def __repr__(self):
        return 'Key({:}, {:})'.format(self.keyval, self.keytype)


class Layer:
    """Hold all key assignments for one layer.

    """

    def __init__(self, size, keys=None):
        self.rows, self.columns = size
        self.keys = [
            [None for c in range(self.columns)]
            for r in range(self.rows)
        ]

        if keys:
            for coords, key in keys:
                x, y = coords
                self.keys[y][x] = key


    def commands(self, z):
        """Yield one uniqueksetkey command per key in the layout.

        """

        for r in range(self.rows):
            for c in range(self.columns):
                key = self.keys[r][c]

                if key is None:
                    key = Key(0, KeyType.NORMAL)

                yield '({:}({:}({:}({:}({:}'.format(
                    c, r, z, key.keyval, key.keytype,
                )


def keycodesfromfile(file):
    ret = dict()

    for line in file:
        line = line.rstrip()

        if not line:
            continue

        try:
            name, keyval, keytype = line.split('\t')
        except ValueError:
            print('Invalid line:', line)
            continue

        keyval = int(keyval)
        keytype = int(keytype)

        ret[name] = Key(keyval, keytype)

    return ret


def layoutfromfile(file, layersize, filter, reverse, keycodes):
    unknowncodes = set()
    layers = dict()
    curlayer = None

    for linenum, line in enumerate(file, start=1):
        line = line.rstrip()

        if not line:
            continue

        if line.upper().startswith('LAYOUT '):
            parts = line.split()
            if len(parts) < 3:
                raise ValueError(
                    'invalid layer format',
                    linenum,
                    line,
                )

            layernum = int(parts[1])
            tag = parts[2]

            if (filter is None) or (tag == filter):
                if layernum in layers:
                    raise ValueError(
                        'layer already defined',
                        linenum,
                        layernum,
                    )

                curlayer = Layer(layersize)
                layers[layernum] = curlayer
                row = 0

            else:
                curlayer = None

            continue

        if curlayer is None:
            continue

        if row >= layersize[0]:
            raise ValueError(
                'too many rows',
                linenum,
                row,
            )

        parts = line.split('\t')

        for col, keyname in enumerate(parts):
            if not keyname:
                continue

            key = None
            if keyname in keycodes:
                key = keycodes[keyname]

            elif keyname.startswith('CUSTOM_'):
                subparts = keyname.split('_')
                if len(subparts) != 3:
                    raise ValueError(
                        'invalid CUSTOM key format',
                        linenum,
                        keyname,
                    )

                key = Key(
                    int(subparts[1]),
                    int(subparts[2]),
                )

            if key is not None:
                if reverse:
                    col = layersize[1] - 1 - col
                curlayer.keys[row][col] = key
            else:
                unknowncodes.add(keyname)

        row += 1

    return layers, unknowncodes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__description__,
    )

    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
    )

    parser_genlayout = parser.add_argument_group()

    parser_genlayout.add_argument(
        'rows',
        type=int,
        help='Number of rows in the keyboard layout',
    )

    parser_genlayout.add_argument(
        'columns',
        type=int,
        help='Number of columns in the keyboard layout',
    )

    parser_genlayout.add_argument(
        'keycodefile',
        type=argparse.FileType('r'),
        help='Tab-delimited file mapping key names to value and type',
    )

    parser_genlayout.add_argument(
        'layoutfile',
        type=argparse.FileType('r'),
        help="Tab-delimited file containing each layer's key assignments",
    )

    parser_genlayout.add_argument(
        '-c', '--command',
        nargs=1,
        default=['uniqueksetkey'],
        help='Serial command to set a specific key',
        metavar='command',
    )

    parser_genlayout.add_argument(
        '-f', '--filter',
        nargs=1,
        default=[None],
        help='Include only layers that match this tag',
        metavar='tag',
    )

    parser_genlayout.add_argument(
        '-r', '--reverse',
        action='store_true',
        default=False,
        help='Reverse layout columns (useful for flipped designs)',
    )

    parser.add_argument(
        '--checkkeycodes',
        action='store_true',
        default=False,
        help='Check the specified keycode file for duplicate key codes',
    )

    prefs = parser.parse_args()

    keycodes = keycodesfromfile(prefs.keycodefile)

    if prefs.checkkeycodes:
        val2names = collections.defaultdict(set)
        for name, key in keycodes.items():
            val2names[(key.keyval, key.keytype)].add(name)

        for key, names in val2names.items():
            if len(names) != 1:
                print('KEY2CODE', key, sorted(names))

        sys.exit(0)


    layers, unknowncodes = layoutfromfile(
        prefs.layoutfile,
        (prefs.rows, prefs.columns),
        prefs.filter[0],
        prefs.reverse,
        keycodes,
    )

    for layernum, layer in sorted(layers.items()):
        for command in layer.commands(layernum):
            print(prefs.command[0] + command, end=' ')
        print()

    for code in sorted(unknowncodes):
        print('UNKNOWN', repr(code))
