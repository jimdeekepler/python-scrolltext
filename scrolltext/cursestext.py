"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
from os import getenv
import curses
import logging
from .utils import (CharacterScroller,
                    get_linenum, SCROLL_TEXT)

TRUE_CHARACTERS = ["1", "y", "yes"]
VERBOSE = getenv("VERBOSE") in TRUE_CHARACTERS or False
if VERBOSE:
    logging.basicConfig(filename="cursesscroller.log", filemode="w", level=logging.DEBUG)
log = logging.getLogger(__name__)


log.debug("start")

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
    curses.curs_set(0)  # Hide the cursor
    winsize = win.getmaxyx()
    visibile_height = winsize[0] - 1
    visibile_text_length = winsize[1] - (2 if box else 0)
    log.debug("win dimensions: (%d, %d)", visibile_text_length, visibile_height)
    line = get_linenum(3, visibile_height - (1 if box else 0))
    log.debug("screenline %d", line)
    scroller = CharacterScroller(visibile_text_length,
                                 visibile_text_length, SCROLL_TEXT)
    win.addstr(1, 10, "Scroll-Text")
    add_quit_text(win, box, line, visibile_height)
    win.timeout(125)
    for text in scroller:
        win_text = text
        if not box and line == visibile_height:
            win_text = text[:-1]
        win.addstr(line, (1 if box else 0), win_text)
        win.redrawwin()
        if check_quit(win):
            return
        win.redrawwin()


def add_quit_text(win, box, line, visibile_height):
    """
    Adds a hint message to win.
    """
    if not box and line == visibile_height:
        win.addstr(visibile_height - 2, 0, " You can quit with 'q' or 'Q'.")
    else:
        win.addstr(visibile_height, (2 if box else 0), " You can quit with 'q' or 'Q'.")


def check_quit(win):
    """
    :returns: True, if a quit character is entered, False, otherwise.
    :rtype: Boolean
    """
    character = win.getch(4, 0)
    if character != -1:
        log.debug("got key (%d)  type %s", character, type(character))
    if character != -1 and (chr(character) in QUIT_CHARACTERS):
        return True
    return False


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
