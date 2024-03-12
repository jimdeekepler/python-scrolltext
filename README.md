[![Python application](https://github.com/jimdeekepler/python-scrolltext/actions/workflows/python-app.yml/badge.svg)](https://github.com/jimdeekepler/python-scrolltext/actions/workflows/python-app.yml)
[![PyPI version](https://img.shields.io/pypi/v/scrolltext.svg)](https://pypi.org/project/scrolltext/)


## python-scrolltext

### Plain Terminal version

    SCROLL_TEXT="Hello, world." scrolltext

You can select the line via `SCROLL_LINE` variable. Negative values are counting
from bottom to top, e.g. the following selects the 2nd last line in the current
terminal:

    SCROLL_TEXT="Hello, world." SCROLL_LINE=-2 scrolltext


### Curses Version

    SCROLL_TEXT="Hello, world." scrolltext cursestext

In addition to `SCROLL_TEXT` and `SCROLL_LINE` variables, the submodule cursestext
understands the variables `VERBOSE` and `SCROLL_BOX`.

Setting `VERBOSE=1` will create a logfile: 'cursesscroller.log' in the
current directory.

Here is an example:

    SCROLL_BOX=1 SCROLL_LINE=-1 VERBOSE=1 scrolltext cursestext

The box is enabled by default.

In order to not draw the box, you can switch it off by defining the variable
`SCROLL_TEXT` with an empty value or 0, e.g. use

    SCROLL_BOX= SCROLL_LINE=-1 scrolltext cursestext

or

    SCROLL_BOX=0 SCROLL_LINE=-1 scrolltext cursestext


### Scroll right-to-left reading text

Using `SCROLL_DIRECTION=1` makes the text start scrolling from left-side of the terminal.
This is used for right-to-left writing languages.


### Using a different scrolling speed

The scrolling speed can be altered by setting the environment variable `SCROLL_SPEED`
There are 10 different speeds available. These can be selected by choosing a
number between 0 and 9.

Slow scrolling speed (default, if not set)

    SCROLL_SPEED=0 scrolltext


Fastest scrolling speed.

    SCROLL_SPEED=10 scrolltext


## Bugs and quirks

 - does not detect term-resize
 - no colors


## Changes

### v0.0.8

 - doc-comments have never been generated, nor are those validated. (TODO)
 - renamed log-file to "scrolltext.log"
 - uses config file "scrolltextrc"
   \*NIX uses "~/.config/scrolltextrc", windows uses "scrolltextrc" in current directory
