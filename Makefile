SHELL = /bin/sh
PYTHON3 = python3

.PHONY: all clean dist

all:

dist:
	$(PYTHON3) setup.py sdist

clean:
	rm -f -- *.pyc
	rm -f -- *.pyo
	rm -f MANIFEST
	rm -f PKG-INFO
	rm -rf __pycache__
	rm -rf build
	rm -rf dist
