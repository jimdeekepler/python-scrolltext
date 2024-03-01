[![Python application](https://github.com/jimdeekepler/python-scrolltext/actions/workflows/python-app.yml/badge.svg)](https://github.com/jimdeekepler/python-scrolltext/actions/workflows/python-app.yml)


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
