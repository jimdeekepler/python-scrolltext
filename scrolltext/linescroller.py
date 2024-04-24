"""
A simple side scrolling text application.
"""
import logging
import shutil
from time import sleep
from .utils import CLEAR, HOME, IS_WINDOWS, UP_ONE_ROW, CharacterScroller, TermSize

if not IS_WINDOWS:
    from scrolltext.getchtimeout import GetchWithTimeout


DEFAULT_COLOR_TABLE_GREYSCALE_256 = [
        "38,5,232m",
        "38,5,233m",
        "38,5,234m",
        "38,5,235m",
        "38,5,236m",
        "38,5,237m",
        "38,5,238m",
        "38,5,239m",
        "38,5,240m",
        "38,5,241m",
        "38,5,242m",
        "38,5,243m",
        "38,5,244m",
        "38,5,245m",
        "38,5,246m",
        "38,5,247m",
        "38,5,248m",
        "38,5,249m",
        "38,5,250m",
        "38,5,251m",
        "38,5,252m",
        "38,5,253m",
        "38,5,254m",
        "38,5,255m"
        ]
DEFAULT_COLOR_TABLE = DEFAULT_COLOR_TABLE_GREYSCALE_256
last_term_rows = -1  # pylint: disable=C0103 (invalid-name)
log = logging.getLogger(__name__)


def linescroller(cfg):
    """
    Main entry point for linescroller.
    :param cfg: Config object
    :type: configparser.ConfigParser
    """
    getch = None
    if not IS_WINDOWS:
        getch = GetchWithTimeout()
    try:
        _linescroller(getch, cfg)
    except RuntimeError:
        pass
    finally:
        if not IS_WINDOWS:
            getch.cleanup()


def _linescroller(getch, cfg):
    """
    Prints a text in a side-scrolling manner.
    """
    term_size = TermSize(0, 0)
    _update_term_size(term_size)
    use_colors = cfg["main"].getboolean("color")
    argv = {}
    argv["min_scroll_line"] = 0
    scroller = CharacterScroller(cfg, term_size, **argv)
    colortable = DEFAULT_COLOR_TABLE
    colortable_size = len(colortable)

    print(f"{CLEAR}{HOME}", end="")
    if scroller.line > 0:
        _move_to_line(scroller.line)
    cnt = 0
    for text in scroller:
        if scroller.line < term_size.get_rows() - 1:
            win_text = text
        else:
            win_text = text[:-1]
        if use_colors:
            win_text = _apply_colors(win_text, colortable, colortable_size)
        print(win_text, end="\r")
        if IS_WINDOWS:
            sleep(.15)
        else:
            _check_input(getch)
        cnt += 1
        if _update_term_size(term_size):
            print(f"{CLEAR}{HOME}", end="")
            if scroller.line > 0:
                _move_to_line(scroller.line)
    if IS_WINDOWS:
        print(f"{UP_ONE_ROW}", end="")


def _apply_colors(win_text, colortable, colortable_size):
    color_index = 0
    new_text = ""
    for ch in win_text:
        log.debug("color-index: %d  color-code: %s", color_index, colortable[color_index])
        new_text += f"\033[{colortable[color_index]}" + ch
        color_index += 1
        color_index = color_index % colortable_size
    return new_text


def _check_input(getch):
    """
    Use getchtimeout to get a character. If "Q" or "q" is given, then it raises SystemExit
    """
    character = getch.getch(timeout=.1)
    if isinstance(character, int) == int:
        log.debug("Got key '%d'", character)
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


def _update_term_size(term_size):
    global last_term_rows  # pylint: disable=W0603 (global-statement)
    available_rows = shutil.get_terminal_size()[1]
    available_columns = shutil.get_terminal_size()[0] - (1 if IS_WINDOWS else 0)
    term_size.set_size(available_columns, available_rows)
    if last_term_rows == -1:
        last_term_rows = term_size.get_rows()
    if term_size.get_rows() != last_term_rows:
        last_term_rows = term_size.get_rows()
        return True
    return False
