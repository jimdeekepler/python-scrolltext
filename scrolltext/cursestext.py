"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
from os import getenv
import curses
import logging
from .utils import CharacterScroller


logging.basicConfig(filename="cursesscroller.log", filemode="w", level=logging.DEBUG)
log = logging.getLogger(__name__)


log.debug("start")

DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_TEXT = getenv("SCROLL_TEXT") or DEF_SCROLL_TEXT
QUIT_CHARACTERS = ["\x1B", "Q", "q"]


def curses_scroller(win):
    """
    Curses-main: render a text in a side-scrolling manner, using curses.

    :param win: Internal curses based object
    :type win: curses._window
    """
    box = True
    if box:
        win.box()
    is_logging_debug = log.isEnabledFor(logging.DEBUG)
    curses.curs_set(0)  # Hide the cursor
    winsize = win.getmaxyx()
    visibile_height = winsize[0] - 1
    visibile_text_length = winsize[1] - (2 if box else 0)
    log.debug("win dimensions: (%d, %d)", visibile_text_length, visibile_height)
    scroller = CharacterScroller(visibile_text_length, visibile_text_length, SCROLL_TEXT)
    win.addstr(1, 10, "Scroll-Text")
    win.addstr(visibile_height, (2 if box else 0), " You can quit with 'q' or 'Q'.")
    win.timeout(125)
    for text in scroller:
        win_text = text
        win.addstr(3, (1 if box else 0), win_text)
        win.redrawwin()
        character = win.getch(4, 0)
        if is_logging_debug and character != -1:
            log.debug("got key (%d)  type %s", character, type(character))
        if character != -1 and (chr(character) in QUIT_CHARACTERS):
            return
        win.redrawwin()


def main():
    """Main usese curses.wrapper. See curses doc for details.
    """
    try:  # noqa: C901 ignoring 'TryExcept 42' is too complex - fix later
        wrapper(curses_scroller)
    except error as ex:
        log.exception(ex)
    finally:
        log.debug("end")


if __name__ == "__main__":
    main()
