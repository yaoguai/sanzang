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

""" Sanzang Utils program module for string substitution. """


import getopt
import io
import signal
import sys
import unicodedata


USAGE = """Usage: szu-ss [options] table_file [file ...]

Table-based string substitution.

Options
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


def read_ss_table(table_fd):
    """
    Read a two-column translation table file for substitutions.

    Given an open file object, read and return the contents of a two-column
    translation table. If uppercase or lowercase variants of the source
    term are available, add records for these variants automatically. For a
    record with more than two columns, a RuntimeError exception is raised.

    """
    tab = []
    table_str = unicodedata.normalize('NFC', table_fd.read())
    for line in table_str.split('\n'):
        rec = [f.strip() for f in line.split('|')]
        if len(rec) == 2:
            tab.append(rec)
            term1, term2 = rec
            term1_lower = term1.lower()
            term1_upper = term1.upper()
            if term1 != term1_lower:
                tab.append([term1_lower, term2.lower()])
            if term1 != term1_upper:
                tab.append([term1_upper, term2.upper()])
        elif line.strip() != '':
            raise RuntimeError('Table error: ' + line.strip())
    return tab


def subst(table, text):
    """
    Make string substitutions using a two-column table.

    The table specified should already contain any uppercase and lowercase
    variants that should be applied for substitution.

    """
    text = unicodedata.normalize('NFC', text)
    for term1, term2 in table:
        if term1 in text:
            text = text.replace(term1, term2)
    return text


def subst_file(table, fd_in, fd_out, buffer_size=1000):
    """
    Make string substitutions from file to file (buffered).

    Given the contents of a two-column translation table, along with input
    and output file objects, make one-to-one string substitutions using
    buffered I/O.

    """
    str_buf = ''
    line_no = 1
    for line in fd_in:
        str_buf += line
        if line_no % buffer_size == 0:
            fd_out.write(subst(table, str_buf))
            str_buf = ''
        line_no += 1
    fd_out.write(subst(table, str_buf))


def main(argv):
    """
    Run as a portable command-line program.

    This program handles data through standard I/O streams as UTF-8 text.
    Input has any leading byte-order marks stripped out from the beginning
    of the input stream. Broken pipes and SIGINT are handled silently.

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
        if len(args) < 1:
            sys.stderr.write(USAGE)
            return 1
        with open(args[0], encoding='utf-8-sig') as table_fd:
            table = read_ss_table(table_fd)
        if len(args) == 1:
            if sys.stdin.isatty():
                subst_file(table, sys.stdin, sys.stdout, buffer_size=1)
            else:
                subst_file(table, sys.stdin, sys.stdout)
        else:
            for file_path in args[1:]:
                with open(file_path, 'r', encoding='utf-8-sig') as fin:
                    subst_file(table, fin, sys.stdout)
        return 0
    except KeyboardInterrupt:
        print()
        return 1
    except Exception as err:
        if verbose:
            raise
        else:
            sys.stderr.write('szu-ss: ' + str(err) + '\n')
            return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
