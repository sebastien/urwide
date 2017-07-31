#!/usr/bin/env python
# encoding: utf8
# -----------------------------------------------------------------------------
# Project   : Mercurial-Easy
# -----------------------------------------------------------------------------
# Author    : Sebastien Pierre                               <sebastien@ivy.fr>
# License   : Revised BSD License
# -----------------------------------------------------------------------------
# Creation  : 31-Jul-2017
# Last mod  : 31-Jul-2017
# -----------------------------------------------------------------------------

import sys ; sys.path.insert(0, "src")
from distutils.core import setup

SUMMARY     = "High-Level interface and DSL to create console interfaces"
DESCRIPTION = """\
The main idea behind URWIDE is to extend URWID with a *domain-specific language
to describe console-based interfaces*, drastically reducing the amount of code
required to create console-based applications.
"""
# ------------------------------------------------------------------------------
#
# SETUP DECLARATION
#
# ------------------------------------------------------------------------------

setup(
    name         = "urwide",
    version      = "1.0.0",
    author       = "Sebastien Pierre", author_email = "sebastien.pierre@gmail.com",
    description   = SUMMARY, long_description  = DESCRIPTION,
    license      = "Revised BSD License",
    keywords     = "tool, interface, gui, command-line",
    url          = "https://github.com/sebastien/urwide",
    package_dir  = { "": "src" },
    modules_dir  = { "": "src" },
    py_modules   = ["urwide"],
)

# EOF - vim: tw=80 ts=4 sw=4 noet

