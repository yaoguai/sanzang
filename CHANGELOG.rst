Change Log
==========

1.3.3 (2016-01-??)
------------------
* Added more helpful and verbose output to szu-ed.
* Removed table format checks from all tools except szu-ed.

1.3.2 (2015-04-01)
------------------
* Reimplemented core algorithm for szu-r (cleaner and faster).
* Added missing delimiter in buffering algorithm for szu-r.
* Added a bit of missing Unicode normalization to szu-r.
* Edited writing message for szu-ed to include the line count.

1.3.1 (2015-03-24)
------------------
* Fixed input_lines support in szu_ed.py so editing terminates normally.
* Added a "file written" message to szu-ed. File writing is important...

1.3.0 (2015-03-11)
------------------
* Converted all programs into Python modules that can be imported.
* Refactored modules for more convenient use in calling code.
* Converted Makefile install / uninstall to use pip3.
* New directory layout (but installation to the same directories).
* Updated documentation for new installation procedure.

1.2.3 (2015-02-16)
------------------
* More thorough Unicode normalization for the table editor (szu-ed).

1.2.2 (2015-02-02)
------------------
* Added basic Unicode normalization for safety and compatibility.

1.2.1 (2015-01-06)
------------------
* Fixed formatting for an example in the szu-t manual page.
* Documentation updates for README.

1.2.0 (2015-01-05)
------------------
* szu-ss: read and process one line at a time if stdin is a TTY.
* szu-t: read and process one line at a time if stdin is a TTY.
* szu-t: at EOF, do not translate the buffer if it is an empty string.

1.1.2 (2015-01-03)
------------------
* szu-ss updated with major performance improvements (~200-300%).
* szu-ss "verbose" option fixed to function correctly.
* Verbose modes now preserve the original stack trace for debugging.

1.1.1 (2014-11-22)
------------------
* szu-ss fixed to show usage if there are too few arguments.
* Tutorial updated to use new listing notation.

1.1.0 (2014-10-31)
------------------
* Added support for input files as positional arguments to commands.
* Changed szu-t list notation to be more compact to aid readability.
* Added a makefile note about setting parameters for BSD, Solaris, etc.
* Programs updated to close a table file immediately after reading it.

1.0.5 (2014-10-02)
------------------
* Makefile dist target now just builds a Python dist.
* Removed superfluous exception handling.
* Updated source code according to pep8 and pep257.
* Documentation fixes and updates.

1.0.4 (2014-09-09)
------------------
* Updated programs for proper universal newline support.
* Fixed makefile logic bug (documentation directory removal).

1.0.3 (2014-08-23)
------------------
* Translation table fields have surrounding whitespace stripped.
* All spaces and tabs will not be removed from table fields.
* Fixed bug in szu-ss so string matching works correctly.
* Minor documentation fixes.

1.0.2 (2014-08-15)
------------------
* Updated szu-ed to print to stderr for any common exceptions.
* Added missing option description for szu-ss.
* Documentation and build system updates and fixes.

1.0.1 (2014-08-11)
------------------
* Tutorial updated to HTML5.
* Documentation copyedits and formatting.
* Added MANIFEST.in to include makefile in the Python package.
* Fixed minor encoding compatibility issues with UTF-8 BOMs.
* Improved szu-ss table-loading code to be more robust.
* Overhauled szu-ss to use buffering -- much more efficient.

1.0.0 (2014-08-10)
------------------
* Initial commit into git.
