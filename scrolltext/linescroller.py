"""
A simple side scrolling text application.
"""
import shutil
from time import sleep
from .utils import CLEAR, HOME, IS_WINDOWS, UP_ONE_ROW, CharacterScroller, init_utils

if not IS_WINDOWS:
    from scrolltext.getchtimeout import GetchWithTimeout


VISIBILE_TEXT_LENGTH = shutil.get_terminal_size()[0]


def linescroller(write_config):
    """
    Main entry point for linescroller.
    :param write_config: Write initial config
    :type: bool
    """
    getch = None
    if not IS_WINDOWS:
        getch = GetchWithTimeout()
    try:
        _linescroller(getch, write_config)
    except RuntimeError:
        pass
    finally:
        if not IS_WINDOWS:
            getch.cleanup()


def _linescroller(getch, write_config):
    """
    Prints a text in a side-scrolling manner.
    """
    cfg = init_utils(write_config)
    argv = {}
    argv["term_rows"] = shutil.get_terminal_size()[1]
    argv["term_columns"] = shutil.get_terminal_size()[0]
    argv["min_scroll_line"] = 0
    scroller = CharacterScroller(cfg, **argv)

    print(f"{CLEAR}{HOME}", end="")
    if scroller.line > 0:
        _move_to_line(scroller.line)
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
