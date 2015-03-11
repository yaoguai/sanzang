#!/usr/bin/env python3
#
# Copyright (c) 2014 the Sanzang Utils authors
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

""" Sanzang Utils program module for CJK translation. """


import getopt
import io
import signal
import sys
import unicodedata


USAGE = """Usage: szu-t [options] table_file [file ...]

Translate CJK text using a translation table.

Options:
  -h, --help       print this help message and exit
  -v, --verbose    include information useful for debugging

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


def read_table(table_fd):
    """
    Read a translation table from an opened file.

    Given an open file object, read a well-formatted translation table and
    return its contents to the caller. If an individual record is formatted
    incorrectly, then a RuntimeError will be raised.

    """
    tab = []
    width = -1
    table_str = unicodedata.normalize('NFC', table_fd.read())
    for line in table_str.split('\n'):
        rec = [f.strip() for f in line.split('|')]
        if width != -1 and width == len(rec):
            tab.append(rec)
        elif width == -1 and len(rec) > 1:
            width = len(rec)
            tab.append(rec)
        elif line.strip() != '':
            raise RuntimeError('Table error: ' + line.strip())
    return tab


def vocab(table, text):
    """
    Return a new table containing only the vocabulary in the source text.

    Create a new translation table containing only the rules that are
    relevant for the given text. This is created by checking all source
    terms against a copy of the text.

    """
    text_rules = []
    text_copy = str(text)
    for rec in table:
        if rec[0] in text_copy:
            text_copy = text_copy.replace(rec[0], '\x1f')
            text_rules.append(rec)
    return text_rules


def tr_raw(table, text):
    """
    Translate text using a table. Return raw texts in a list.

    Perform translation of a text by applying the rules in a translation
    table. The result is a list of strings with each element corresponding
    to a column in the translation table.

    """
    text = unicodedata.normalize('NFC', text).replace('\x1f', '')
    rules = vocab(table, text)
    collection = [text]
    for col_no in range(1, len(table[0])):
        trans = text
        for rec in rules:
            trans = trans.replace(rec[0], '\x1f' + rec[col_no] + '\x1f')
        trans = trans.replace('\x1f\n', '\n')
        trans = trans.replace('\x1f\x1f', ' ')
        trans = trans.replace('\x1f', ' ')
        collection.append(trans)
    return collection


def tr_fmt(table, buffer, start):
    """
    Translate text using a table. Return a formatted listing string.

    Perform translation of a text by applying rules in a translation table,
    and return a formatted string. The formatted string represents the
    source text and its translations collated together and organized by
    line number and by translation table column number.

    """
    collection = tr_raw(table, buffer)
    for i in range(0, len(collection)):
        collection[i] = collection[i].rstrip().split('\n')
    listing = ''
    for line_no in range(0, len(collection[0])):
        for col_idx in range(0, len(table[0])):
            listing += '%d.%d|%s\n' % (
                start + line_no,
                col_idx + 1,
                collection[col_idx][line_no])
        listing += '\n'
    return listing


def tr_file(table, fd_in, fd_out, start_idx=1, buf_size=100):
    """
    Translate from one file to another (buffered).

    Given a table, an input file object, and an output file object, apply
    the translation table rules to the input text and write the translation
    as a formatted string to the output.

    """
    str_buf = ''
    line_no = start_idx
    for line in fd_in:
        str_buf += line
        if line_no % buf_size == 0:
            fd_out.write(tr_fmt(table, str_buf, line_no - buf_size + 1))
            str_buf = ''
        line_no += 1
    if len(str_buf) > 0:
        position = line_no - str_buf.count('\n')
        fd_out.write(tr_fmt(table, str_buf, position))
    return line_no


def main(argv):
    """
    Run as a portable command-line program.

    This program reads and writes UTF-8 text, and uses standard I/O streams
    for input text and translation output. Input has any leading byte-order
    marks stripped out from the beginning of the input stream. Broken pipes
    and SIGINT are handled silently.

    """
    set_stdio_utf8()

    if 'SIGPIPE' in dir(signal):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    verbose = False
    try:
        opts, args = getopt.getopt(argv[1:], 'hv', ['help', 'verbose'])
        for option, _ in opts:
            if option in ('-h', '--help'):
                print(USAGE, end='')
                return 0
            if option in ('-v', '--verbose'):
                verbose = True
        if len(args) < 1:
            sys.stderr.write(USAGE)
            return 1
        with open(args[0], 'r', encoding='utf-8-sig') as table_fd:
            table = read_table(table_fd)
        if len(args) == 1:
            if sys.stdin.isatty():
                tr_file(table, sys.stdin, sys.stdout, start_idx=1, buf_size=1)
            else:
                tr_file(table, sys.stdin, sys.stdout)
        else:
            idx = 1
            for file_path in args[1:]:
                with open(file_path, 'r', encoding='utf-8-sig') as fin:
                    idx = tr_file(table, fin, sys.stdout, idx)
        return 0
    except KeyboardInterrupt:
        print()
        return 1
    except Exception as err:
        if verbose:
            raise
        else:
            sys.stderr.write('szu-t: ' + str(err) + '\n')
            return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
