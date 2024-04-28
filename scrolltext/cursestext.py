"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
import curses
import logging
from .utils import CharacterScroller, IS_WINDOWS, TermSize

import _curses

QUIT_CHARACTERS = ["\x1B", "Q", "q"]


log = logging.getLogger(__name__)


def curses_scroller(win, cfg):
    """
    Curses-main: render a text in a side-scrolling manner, using curses.

    :param win: Internal curses based object
    :type win: curses._window
    :param cfg: Config object
    :type: configparser.ConfigParser
    """
    if not IS_WINDOWS:
        curses.curs_set(0)  # Hide the cursor

    term_size = TermSize(0, 0)
    update_term_size(win, cfg["cursestext"].getboolean("box"), term_size)
    argv = {}
    argv["min_scroll_line"] = 3
    scroller = CharacterScroller(cfg, term_size, **argv)
    draw_items(win, cfg["cursestext"].getboolean("box"),
               argv["min_scroll_line"], scroller, term_size)

    win.timeout(100)
    try:
        do_textloop(win, cfg, term_size, scroller, argv["min_scroll_line"])
    except KeyboardInterrupt:
        pass


def do_textloop(win, cfg, term_size, scroller, min_scroll_line):
    """
    This method loops over the scrolled text
    """
    box = cfg["cursestext"].getboolean("box")
    term_too_small_printed = False
    for text in scroller:
        win_text = text
        # hack: When writing to the last line we prevent adding an immediate newline and thus
        #       moving the text upwards, by removing the last character of the visibile text.
        if not box and scroller.line == term_size.get_rows():
            win_text = text[:-1]
        if scroller.line >= min_scroll_line:
            _addstr_wrapper(win, scroller.line, (1 if box else 0), win_text)
            term_too_small_printed = False
            win.redrawwin()
        else:
            if not term_too_small_printed:
                log.debug("Terminal is too small  cols: %d  rows: %d",
                          term_size.get_cols(), term_size.get_rows())
            term_too_small_printed = True
        character = get_char(win)
        if character == curses.KEY_EXIT:
            return
        if character == curses.KEY_RESIZE:
            update_term_size(win, box, term_size)
            draw_items(win, box, min_scroll_line, scroller, term_size)


def add_quit_text(win, box, line, term_size):
    """
    Adds a hint message to win.
    """
    if term_size.get_cols() < len(" You can quit with 'q' or 'Q'.") + 2:
        return
    if not box and line == term_size.get_rows():
        _addstr_wrapper(win, term_size.get_rows() - 2, 0, " You can quit with 'q' or 'Q'.")
    else:
        _addstr_wrapper(win, term_size.get_rows(),
                        (2 if box else 0), " You can quit with 'q' or 'Q'.")


def get_char(win):
    """
    :returns: curses.KEY_EXIT, if a quit character is entered, the current character, otherwise.
    :rtype: int
    """
    log.debug("getch")
    character = None
    character = win.getch(0, 0)
    if character != -1:
        log.debug("got key (%d)  type %s", character, type(character))
    if character != -1 and (chr(character) in QUIT_CHARACTERS):
        return curses.KEY_EXIT
    return character


def update_term_size(win, box, term_size):
    """
    Updates TermSize object.
    """
    winsize = win.getmaxyx()
    log.debug("win dimensions: (columns, rows) (%d, %d)", winsize[1], winsize[0])
    available_rows = winsize[0] - (2 if box else 1)
    available_columns = winsize[1] - (2 if box else 0)
    term_size.set_size(available_columns, available_rows)


def draw_items(win, box, min_scroll_line, scroller, term_size):
    """
    Add strings to the curses window.
    """
    # clear the window contents
    win.clear()
    if box:
        win.box()

    # and redraw screen
    if scroller.line != 1 and term_size.get_cols() > len("Scroll-Text"):
        _addstr_wrapper(win, 1, 10, "Scroll-Text")
    if term_size.get_rows() > min_scroll_line:
        add_quit_text(win, box, scroller.line, term_size)


def _addstr_wrapper(win, row, column, text):
    log.debug("addstr to line %d", row)
    try:
        win.addstr(row, column, text)
    except _curses.error:
        log.exception("Error in addstr")


def work(cfg):
    """Main usese curses.wrapper. See curses doc for details.
    """
    try:  # noqa: C901 ignoring 'TryExcept 42' is too complex - fix later
        wrapper(curses_scroller, cfg)
    except error as ex:
        log.exception(ex)
    finally:
        log.debug("end")
