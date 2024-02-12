"""
A simple side scrolling text application.
"""
import shutil
import sys
from os import getenv
from .utils import CharacterScroller
from .utils import CLEAR, HOME


IS_WINDOWS = sys.platform in ["msys", "win32", "nt"]
if not IS_WINDOWS:
    from .getchtimeout import GetchWithTimeout
else:
    from time import sleep


DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_TEXT = getenv("SCROLL_TEXT") or DEF_SCROLL_TEXT
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
    scroller = CharacterScroller(VISIBILE_TEXT_LENGTH, VISIBILE_TEXT_LENGTH, SCROLL_TEXT)
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
    if character is not None and character in ["Q", "q"]:
        raise RuntimeError()


if __name__ == "__main__":
    linescroller()
