#!/usr/bin/env python3

""" Sanzang Utils setup script for packaging and installation. """

from distutils.core import setup

with open('README.rest', 'r', encoding='utf-8') as fin:
    LONG_DESCRIPTION = fin.read()

setup(
    #
    # Basic information
    #
    name='sanzang-utils',
    version='1.2.3',
    author='yaoguai',
    author_email='lapislazulitexts@gmail.com',
    url='https://github.com/yaoguai/sanzang-utils',
    license='MIT',
    #
    # Descriptions & classifiers
    #
    description='Machine Translation from Chinese, Japanese, or Korean.',
    long_description=LONG_DESCRIPTION,
    keywords='chinese japanese korean cjk asia language machine translation',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Religion',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities'],
    #
    # Included Python files
    #
    scripts=[
        'bin/szu-ed',
        'bin/szu-r',
        'bin/szu-ss',
        'bin/szu-t'],
    data_files=[
        ('share/doc/sanzang-utils', [
            'AUTHORS.rest',
            'LICENSE.rest',
            'NEWS.rest',
            'README.rest',
            'TUTORIAL.html']),
        ('share/man/man1', [
            'man1/szu-ed.1',
            'man1/szu-r.1',
            'man1/szu-ss.1',
            'man1/szu-t.1'])]
)
