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

""" Sanzang Utils program module for reformatting CJK text. """


import getopt
import io
import re
import signal
import sys
import unicodedata


USAGE = """Usage: szu-r [options] [file ...]

Reformat CJK text for translation.

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


def reflow(text):
    """
    Reformat CJK text according to its punctuation.

    Given a string, this function will reformat ("reflow") the text so that
    words and terms are not broken apart between lines. The function first
    strips out any leading margins as used by CBETA texts. It then
    collapses all line breaks, and reformats the text according to
    horizontal spacing and punctuation.

    CBETA margin format: X01n0020_p0404a01(00)║

    """
    # Remove CBETA margins.
    text = re.sub(r'^[T|X].*?║', '', text, flags=re.M)

    # Separate poetry from prose. If the line is short and starts with a space,
    # then add another space at the end to separate it from the following text.
    #
    text = re.sub(r'^　(.{1,15})$', '　\\1　', text, flags=re.M)

    # Collapse newlines.
    text = text.replace('\n', '')

    # Ender followed by non-ender: newline in between.
    text = re.sub(
        r'([：，；。？！」』.;:\?\!])([^：，；。？！」』.;:\?\!])',
        '\\1\n\\2', text, flags=re.M)

    # Non-starter, non-ender, followed by a starter: newline in between.
    text = re.sub(
        r'([^「『　\t：，；。？！」』.;:\?\!\n])([「『　\t])',
        '\\1\n\\2', text, flags=re.M)

    # Adjust newlines and return.
    if len(text) > 0 and text[-1] != '\n':
        text += '\n'
    return text


def reflow_file(fd_in, fd_out, buffer_size=1000):
    """
    Reformat CJK text from one file object to another.

    Given input and output file objects, reformat CJK text from one to the
    other according to the punctuation and horizontal spacing. I/O is
    buffered for higher performance.

    """
    enders = '：，；。？！」』.;:?'
    str_buf = ''
    line_n = 0

    for line in fd_in:
        line_n += 1
        str_buf = str_buf + line
        if line_n % buffer_size == 0:
            i = len(str_buf) - 1
            while i > 0:
                if str_buf[i-1] in enders and str_buf[i] not in enders:
                    norm_buffer = unicodedata.normalize('NFC', str_buf[:i])
                    fd_out.write(reflow(norm_buffer))
                    str_buf = str_buf[i:]
                    i = -1
                else:
                    i = i - 1
    if len(str_buf) > 0:
        fd_out.write(reflow(str_buf))


def main(argv):
    """
    Run szu-r as a portable command-line program.

    This program will attempt to handle data through standard I/O streams
    as UTF-8 text. Input text will have a leading byte-order mark stripped
    out if one is found. Broken pipes and SIGINT are handled silently.

    """
    set_stdio_utf8()

    if 'SIGPIPE' in dir(signal):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    try:
        verbose = False
        opts, args = getopt.getopt(argv[1:], 'hv', ['help', 'verbose'])
        for option, _ in opts:
            if option in ('-h', '--help'):
                print(USAGE, end='')
                return 0
            if option in ('-v', '--verbose'):
                verbose = True
        if len(args) == 0:
            reflow_file(sys.stdin, sys.stdout)
        else:
            for file_path in args:
                with open(file_path, 'r', encoding='utf-8-sig') as fin:
                    reflow_file(fin, sys.stdout)
        return 0
    except KeyboardInterrupt:
        print()
        return 1
    except Exception as err:
        if verbose:
            raise
        else:
            sys.stderr.write('szu-r: ' + str(err) + '\n')
            return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
