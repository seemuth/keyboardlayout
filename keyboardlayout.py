#!/usr/bin/env python3

"""
Keyboard layout generator.

Usage:
    layout.py <rows> <columns> <keycodefile> [--filter=<tag>] <layoutfile>
    layout.py (-h | --help)
    layout.py --version

Options:
    -h --help       Show this screen.
    --version       Show version.
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

import docopt
import sys


__version__ = '0.1.0'

__title__ = 'keyboardlayout'
__author__ = 'Daniel P. Seemuth'
__description__ = 'Keyboard layout generator for keyboards from uniquekeyboard.com'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Daniel P. Seemuth'


if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=__version__)
    print(args)
