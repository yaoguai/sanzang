Sanzang
=======

**GitHub:** <https://github.com/yaoguai/sanzang>

Sanzang is a compact and simple cross-platform set of CAT utilities. These
are especially useful for translating from CJK languages (Chinese, Japanese,
and Korean).

Due to its origins in translating texts from the Chinese Buddhist canon, this
translation system is called Sanzang (三藏), a literal translation of the
Sanskrit word "Tripitaka," which is a general term for the Buddhist canon. As
demonstrated by the Sanzang translator itself::

    $ echo 三藏 | szu-t sztab
    1.1|三藏
    1.2| sānzàng
    1.3| tripiṭaka

Anyone can learn how to use Sanzang, and use these programs to read and analyze
texts. Unlike other systems, Sanzang is small and approachable. You can easily
develop your own translation rules, and these rules are just stored in a text
file and applied at runtime.

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
then Cygwin is the best environment for these programs. To install Sanzang,
you can use *pip3* to install it::

    # pip3 install .
