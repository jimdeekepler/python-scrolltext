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

This will create a logfile: 'cursesscroller.log' in the current directory.

