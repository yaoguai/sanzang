#!/usr/bin/env python3
#
# Copyright (c) 2014-2015 the Sanzang Utils authors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Sanzang Utils program module for table editing. """


import getopt
import io
import os
import signal
import sys
import unicodedata

try:
    import readline
except ImportError:
    pass


USAGE = """Usage: szu-ed [options] table_file

Edit translation table rules using a program of simple commands.

Options:
  -h, --help       print this help message and exit

"""


def set_stdio_utf8():
    """
    Set standard I/O streams to UTF-8.

    Attempt to reassign standard I/O streams to new streams using UTF-8.
    Standard input should discard any leading BOM. If an error is raised,
    assume the environment is inflexible but correct (IDLE).

    """
    try:
        sys.stdin = io.TextIOWrapper(
            sys.stdin.detach(), encoding='utf-8-sig', line_buffering=True)
        sys.stdout = io.TextIOWrapper(
            sys.stdout.detach(), encoding='utf-8', line_buffering=True)
        sys.stderr = io.TextIOWrapper(
            sys.stderr.detach(), encoding='utf-8', line_buffering=True)
    except io.UnsupportedOperation:
        pass


def read_table(tab_str):
    """
    Read a translation table from a formatted string.

    Given a translation table as a formatted string, load the contents and
    return them as a dictionary. The keys are source terms (column 1),
    while each value is a list of the corresponding terms.

    """
    tab_str = unicodedata.normalize('NFC', tab_str)
    tab = {}
    width = -1
    for line in tab_str.split('\n'):
        rec = [f.strip() for f in line.split('|')]
        if width != -1 and width == len(rec):
            tab[rec[0]] = rec[1:]
        elif width == -1 and len(rec) > 1:
            width = len(rec)
            tab[rec[0]] = rec[1:]
        elif line.strip() != '':
            raise RuntimeError('Table error: ' + line.strip())
    return tab, width


def table_to_str(tab):
    """
    Produce a formatted string for a translation table.

    Given a table stored as a dictionary, sort the contents and return the
    table as text in the translation table format for storage.

    """
    table_str = ''
    items = list(tab.items())
    items.sort(key=lambda x: (-len(x[0]), x[0]))
    for i in items:
        table_str += i[0] + '|' + '|'.join(i[1]) + '\n'
    return table_str


def edit(table_fpath, input_lines=None):
    """
    Open a translation table and run editor commands.

    Editor commands are read from standard input by default, and non-error
    output is written to standard output. Errors are printed to standard
    error. If a list of input lines is also specified, then read editor
    input from this list instead of the standard input.

    """
    if not os.path.exists(table_fpath):
        open(table_fpath, 'w', encoding='utf-8').close()
        tab, width = read_table('')
    else:
        with open(table_fpath, 'r', encoding='utf-8-sig') as fin:
            tab, width = read_table(fin.read())
    cmd = '\\set'
    try:
        while True:
            if input_lines is None:
                line = unicodedata.normalize('NFC', input().strip())
            elif len(input_lines) > 0:
                line = unicodedata.normalize('NFC', input_lines.pop(0).strip())
            else:
                return
            if line in ('\\get', '\\rm', '\\set'):
                cmd = line
            elif line == '\\p':
                print(table_to_str(tab), end='')
            elif line == '\\q':
                return
            elif line == '\\w' or line == '\\wq':
                with open(table_fpath, 'w', encoding='utf-8') as fout:
                    fout.write(table_to_str(tab))
                sys.stderr.write('"%s" (%d lines)\n' % (table_fpath, len(tab)))
                if line == '\\wq':
                    return
            elif line != '' and not line.startswith('\\'):
                if cmd == '\\get':
                    try:
                        print('%s|%s' % (line, '|'.join(tab[line])))
                    except KeyError:
                        sys.stderr.write('Not found: ' + line + '\n')
                elif cmd == '\\rm':
                    try:
                        del tab[line]
                    except KeyError:
                        sys.stderr.write('Not found: ' + line + '\n')
                elif cmd == '\\set':
                    toks = [f.strip() for f in line.split('|')]
                    if width == -1 and len(toks) > 1:
                        width = len(toks)
                    if len(toks) == width:
                        tab[toks[0]] = toks[1:]
                    else:
                        sys.stderr.write('Invalid assignment: ' + line + '\n')
            elif line.strip() == '':
                pass
            else:
                sys.stderr.write('Syntax error: ' + line + '\n')
    except EOFError:
        return


def main(argv):
    """
    Run szu-ed as a portable command-line program.

    This program handles data through standard I/O streams as UTF-8 text.
    Input has any leading byte-order mark stripped if one is found. Broken
    pipes and SIGINT are handled silently.

    """
    set_stdio_utf8()
    if 'SIGPIPE' in dir(signal):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        opts, args = getopt.getopt(argv[1:], 'h', ['help'])
        for option, _ in opts:
            if option in ('-h', '--help'):
                print(USAGE, end='')
                return 0
        if len(args) != 1:
            sys.stderr.write(USAGE)
            return 1
        edit(args[0])
        return 0
    except getopt.GetoptError:
        sys.stderr.write(USAGE)
        return 1
    except KeyboardInterrupt:
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
