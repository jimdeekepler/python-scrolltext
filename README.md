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
