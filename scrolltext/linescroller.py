"""
A simple side scrolling text application.
"""
import shutil
from time import sleep
from .utils import (CLEAR, HOME, IS_WINDOWS, UP_ONE_ROW, CharacterScroller, get_linenum,
                    SCROLL_TEXT, scroll_direction, scrollspeedsec)


if not IS_WINDOWS:
    from .getchtimeout import GetchWithTimeout


VISIBILE_TEXT_LENGTH = shutil.get_terminal_size()[0]


def linescroller():
    """
    Main entry point for linescroller.
    """
    getch = None
    if not IS_WINDOWS:
        getch = GetchWithTimeout()
    try:
        _linescroller(getch)
    except RuntimeError:
        pass
    finally:
        if not IS_WINDOWS:
            getch.cleanup()


def _linescroller(getch):
    """
    Prints a text in a side-scrolling manner.
    """
    print(f"{CLEAR}{HOME}", end="")
    line = get_linenum(0,  shutil.get_terminal_size()[1])
    if line > 0:
        _move_to_line(line)
    scroller = CharacterScroller(VISIBILE_TEXT_LENGTH, VISIBILE_TEXT_LENGTH,
                                 SCROLL_TEXT, scroll_direction, scrollspeedsec)
    for text in scroller:
        win_text = text
        print(win_text, end="\r")
        if IS_WINDOWS:
            sleep(.15)
        else:
            _check_input(getch)
    if IS_WINDOWS:
        print(f"{UP_ONE_ROW}", end="")


def _check_input(getch):
    """
    Use getchtimeout to get a character. If "Q" or "q" is given, then it raises SystemExit
    """
    character = getch.getch(timeout=.1)
    if character is not None and character in ["\033", "\x1b", "", "\r", "", " ", "Q", "q"]:
        raise RuntimeError()


def _move_to_line(line):
    """
    Move the cursor to the specified line. This is done using ANSI Escape sequences.
    :param line: The line number to scroll to.
    :type line: int
    """
    if not IS_WINDOWS:
        print(f"\033[{line}B", end="")
    else:
        for _ in range(line):
            print("\033[1B", end="")
