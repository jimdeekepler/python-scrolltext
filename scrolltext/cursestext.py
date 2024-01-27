"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
from os import getenv
import logging
import shutil
from utils import CharacterScroller


logging.basicConfig(filename="cursesscroller.log", filemode="w", level=logging.DEBUG)
log = logging.getLogger(__name__)


log.debug("start")

DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_TEXT = getenv("SCROLL_TEXT") or DEF_SCROLL_TEXT
VISIBILE_TEXT_LENGTH = shutil.get_terminal_size().columns - 1


def curses_scroller(win):
    """
    Curses-main: render a text in a side-scrolling manner, using curses.

    :param win: Internal curses based object
    :type win: curses._window
    """
    scroller = CharacterScroller(VISIBILE_TEXT_LENGTH, VISIBILE_TEXT_LENGTH, SCROLL_TEXT)
    win.addstr(1, 10, "Scroll-Text")
    win.timeout(125)
    for text in scroller:
        win_text = text
        win.addstr(3, 1, win_text)
        win.redrawwin()
        win.getch(4, 0)
        win.redrawwin()


try:
    wrapper(curses_scroller)
except error as e:
    log.exception(e)
finally:
    log.debug("end")
