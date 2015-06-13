Sanzang Utils
=============

**Website:** <http://lapislazulitexts.com/sanzang>

**GitHub:** <https://github.com/yaoguai/sanzang-utils>

Sanzang is a compact and simple cross-platform machine translation system. This
system is especially useful for translating from CJK languages (Chinese,
Japanese, and Korean). Unlike most other machine translation systems, Sanzang
is useful even for ancient and otherwise difficult texts.

Due to its origins in translating texts from the Chinese Buddhist canon, this
translation system is called Sanzang (三藏), a literal translation of the
Sanskrit word "Tripitaka," which is a general term for the Buddhist canon. As
demonstrated by the Sanzang translator itself::

    $ echo 三藏 | szu-t sztab
    1.1|三藏
    1.2| sānzàng
    1.3| tripiṭaka

Anyone can learn how to use Sanzang Utils, and use these programs to read and
analyze texts. Unlike other systems, Sanzang is small and approachable. You can
easily develop your own translation rules, and these rules are just stored in a
text file and applied at runtime.

Components
----------

Sanzang Utils includes the following programs:

* szu-ed (1) - Command-based translation table editor
* szu-r (1) - Preprocessor for reformatting CJK text
* szu-t (1) - The main translation program
* szu-ss (1) - Case-sensitive string substitution tool

These are all written in Python 3 and available under the MIT License.

Installation
------------

To run these programs, Python 3.x is required. Installation on a Unix-like
platform is advised, but Windows is possible too. If you are using Windows,
then Cygwin is the best environment for these programs. To install Sanzang
Utils, you can call *pip3* to download and install it::

    # pip3 install sanzang-utils

If you do not have *pip3* installed on your system, you can download the
Sanzang Utils software manually and then install it using the old method::

    # python3 setup.py install

Documentation
-------------

After installing Sanzang Utils, you may want to read the introduction and the
tutorial. The introduction introduces you to the core concepts and rationale
behind the system. The tutorial gives practical instruction on exactly how to
use each component, how they relate to one another, and how you can develop
your own translation tables.

**Sanzang Introduction:** <http://lapislazulitexts.com/articles/sanzang_intro>

**Sanzang Utils Tutorial:** <http://lapislazulitexts.com/articles/szu_tutorial>

In addition to the introduction and tutorial, each program also includes a
traditional Unix manual page that can be used as a reference.

Updates
-------

To find out what new fixes and features are available with each new version,
you can check the NEWS file, which lists all notable changes according to the
version number and date.

Versions of Sanzang Utils follow the scheme N.N.N, indicating the major
version, minor version, and the patch number. The patch number is incremented
for sets of small updates or bug fixes, the minor number indicates some new
feature or new behavior, and the major number indicates a big change or new and
incompatible behavior.
