"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
from os import getenv
import logging
import shutil


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
    """
    win.addstr(1, 10, "Scroll-Text")
    win.timeout(125)
    blanks = " " * VISIBILE_TEXT_LENGTH
    blanks_end = " " * 15
    complete_text = blanks + SCROLL_TEXT + blanks_end
    for start in range(len(complete_text)):
        end = start + VISIBILE_TEXT_LENGTH
        win_text = complete_text[start:end]
        win.addstr(3, 1, win_text)
        win.redrawwin()
        win.getch(4, 0)
        win.redrawwin()
        start += 1


try:
    wrapper(curses_scroller)
except error as e:
    log.exception(e)
finally:
    log.debug("end")
