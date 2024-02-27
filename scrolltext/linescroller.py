"""
A simple side scrolling text application.
"""
import shutil
import sys
from time import sleep
from .utils import (CLEAR, HOME, CharacterScroller, get_linenum, SCROLL_TEXT)


IS_WINDOWS = sys.platform in ["msys", "win32", "nt"]
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
        print(f"\033[{line}B", end="")
    scroller = CharacterScroller(VISIBILE_TEXT_LENGTH,
                                 VISIBILE_TEXT_LENGTH, SCROLL_TEXT)
    for text in scroller:
        win_text = text
        print(win_text, end="\r")
        if IS_WINDOWS:
            sleep(.15)
        else:
            _check_input(getch)


def _check_input(getch):
    """
    Use getchtimeout to get a character. If "Q" or "q" is given, then it raises SystemExit
    """
    character = getch.getch(timeout=.15)
    if character is not None and character in ["\033", "\x1b", "", "\r", "", " ", "Q", "q"]:
        raise RuntimeError()


if __name__ == "__main__":
    linescroller()
