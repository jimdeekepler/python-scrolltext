[![Python application](https://github.com/jimdeekepler/python-scrolltext/actions/workflows/python-app.yml/badge.svg)](https://github.com/jimdeekepler/python-scrolltext/actions/workflows/python-app.yml)
[![PyPI version](https://img.shields.io/pypi/v/scrolltext.svg)](https://pypi.org/project/scrolltext/)


## python-scrolltext

A little toy-like app for scrolling text in your favourite terminal.

There is a configuration file "~/.config/scrolltextrc" on UNIX systems and just scrolltextrc in the
current directory when you are using it on a WINDOWS machine. If the config file is not yet
existing, it can be created by passing the command line option: "-w"|"--write", like so:

    scrolltext -w


### Plain Terminal version

    SCROLL_TEXT="Hello, world." scrolltext [linescroller]


### Curses Version

    SCROLL_TEXT="Hello, world." scrolltext cursestext


### Scroll right-to-left reading text

Using `SCROLL_DIRECTION=1` makes the text start scrolling from left-side of the terminal.
This is used for right-to-left writing languages.
<<<<<<< HEAD


### Using a different scrolling speed

The scrolling speed can be altered by setting the environment variable `SCROLL_SPEED`
There are 10 different speeds available. These can be selected by choosing a
number between 0 and 9.

Slow scrolling speed (default, if not set)

    SCROLL_SPEED=0 scrolltext


Fastest scrolling speed.

    SCROLL_SPEED=10 scrolltext


## Bugs and quirks

 - attempts to detect term-resize, and clumsily adjusts some things
 - no colors


## Changes

### v0.0.11

TODO

### v0.0.10

TODO

### v0.0.9

 - attempt to handle term resizes
 - added config-option: endless  (see newly generated config-file)
 - removed logging from main branch (you may find it on the devel branch)

### v0.0.8

 - doc-comments have never been generated, nor are those validated. (TODO)
 - renamed log-file to "scrolltext.log"
 - uses config file "scrolltextrc"
   \*NIX uses "~/.config/scrolltextrc", windows uses "scrolltextrc" in current directory
=======
>>>>>>> 9b37b6f (Removed some documentation...)
