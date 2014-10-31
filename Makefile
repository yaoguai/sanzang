INSTALL = install
SHELL = /bin/sh
PYTHON3 = python3

# The variables below are set to the defaults for Cygwin, Linux, and OS X. If
# you are installing or uninstalling on a different type of system, or using
# non-default locations, then you should specify these as needed. For example,
# if you are installing to "/usr/local" and using BSD or Solaris:
#
# make install prefix=/usr/local mandir=/usr/local/man

prefix = /usr/local
exec_prefix = $(prefix)
bindir = $(exec_prefix)/bin
datarootdir = $(prefix)/share
datadir = $(datarootdir)
docdir = $(datarootdir)/doc/sanzang-utils
mandir = $(datarootdir)/man
man1dir = $(mandir)/man1

.PHONY: all clean dist install uninstall

all:

dist:
	$(PYTHON3) setup.py sdist

install:
	mkdir -p -m 0755 $(bindir)
	mkdir -p -m 0755 $(man1dir)
	mkdir -p -m 0755 $(docdir)
	$(INSTALL) -m 0755 bin/szu-ed $(bindir)
	$(INSTALL) -m 0755 bin/szu-r $(bindir)
	$(INSTALL) -m 0755 bin/szu-ss $(bindir)
	$(INSTALL) -m 0755 bin/szu-t $(bindir)
	$(INSTALL) -m 0644 man1/szu-ed.1 $(man1dir)
	$(INSTALL) -m 0644 man1/szu-r.1 $(man1dir)
	$(INSTALL) -m 0644 man1/szu-ss.1 $(man1dir)
	$(INSTALL) -m 0644 man1/szu-t.1 $(man1dir)
	$(INSTALL) -m 0644 AUTHORS.rest $(docdir)
	$(INSTALL) -m 0644 LICENSE.rest $(docdir)
	$(INSTALL) -m 0644 NEWS.rest $(docdir)
	$(INSTALL) -m 0644 README.rest $(docdir)
	$(INSTALL) -m 0644 TUTORIAL.html $(docdir)

uninstall:
	rm -f $(bindir)/szu-ed
	rm -f $(bindir)/szu-r
	rm -f $(bindir)/szu-ss
	rm -f $(bindir)/szu-t
	rm -f $(man1dir)/szu-ed.1
	rm -f $(man1dir)/szu-r.1
	rm -f $(man1dir)/szu-ss.1
	rm -f $(man1dir)/szu-t.1
	rm -f $(docdir)/AUTHORS.rest
	rm -f $(docdir)/LICENSE.rest
	rm -f $(docdir)/NEWS.rest
	rm -f $(docdir)/README.rest
	rm -f $(docdir)/TUTORIAL.html
	test ! -d $(docdir) || rmdir $(docdir)

clean:
	rm -f -- *.pyc *.pyo */*.pyc */*.pyo
	rm -rf -- __pycache__ */__pycache__
	rm -f MANIFEST
	rm -f PKG-INFO
	rm -rf build
	rm -rf dist
