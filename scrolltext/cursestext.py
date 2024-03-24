"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
import curses
import logging
from .utils import CharacterScroller, IS_WINDOWS


QUIT_CHARACTERS = ["\x1B", "Q", "q"]


log = logging.getLogger(__name__)


def curses_scroller(win, cfg):
    """
    Curses-main: render a text in a side-scrolling manner, using curses.

    :param win: Internal curses based object
    :type win: curses._window
    :param cfg: Config object
    :type: configerparser.ConfigParser
    """
    winsize = win.getmaxyx()
    log.debug("win dimensions: (columns, rows) (%d, %d)", winsize[1], winsize[0])

    box = cfg["cursestext"].getboolean("box")
    # try:
    if box:
        win.box()
    if not IS_WINDOWS:
        curses.curs_set(0)  # Hide the cursor

    argv = {}
    argv["term_rows"] = winsize[0] - (2 if box else 1)
    argv["term_columns"] = winsize[1] - (2 if box else 0)
    argv["min_scroll_line"] = 3
    scroller = CharacterScroller(cfg, **argv)

    win.addstr(1, 10, "Scroll-Text")
    add_quit_text(win, box, scroller.line, argv["term_rows"])
    win.timeout(100)
    try:
        do_textloop(win, box, scroller, argv["term_rows"])
    except KeyboardInterrupt:
        pass


def do_textloop(win, box, scroller, visibile_height):
    """
    This method loops over the scrolled text
    """
    for text in scroller:
        win_text = text
        if not box and scroller.line == visibile_height:
            win_text = text[:-1]
        win.addstr(scroller.line, (1 if box else 0), win_text)
        win.redrawwin()
        if check_quit(win):
            return


def add_quit_text(win, box, line, visibile_height):
    """
    Adds a hint message to win.
    TODO: visibile_height, winsize, ...??
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


def work(cfg):
    """Main usese curses.wrapper. See curses doc for details.
    """
    try:  # noqa: C901 ignoring 'TryExcept 42' is too complex - fix later
        wrapper(curses_scroller, cfg)
    except error as ex:
        log.exception(ex)
    finally:
        log.debug("end")
