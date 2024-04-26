"""
A simple side scrolling text application.
"""
import logging
import shutil
from time import sleep
from .utils import CLEAR, HOME, BOLD, NORMAL, IS_WINDOWS, UP_ONE_ROW, CharacterScroller, TermSize

if not IS_WINDOWS:
    from scrolltext.getchtimeout import GetchWithTimeout


DEFAULT_COLOR_TABLE_GREYSCALE_256 = ["38;5;" + str(x) + "m" for x in range(232,256)]
DEFAULT_COLOR_TABLE_CONSOLE = [str(x) + "m" for x in [30, 34, 35, 36, 31, 32, 33]]
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
    use_bold = False
    use_colors = cfg["main"].getboolean("color")
    argv = {}
    argv["min_scroll_line"] = 0
    scroller = CharacterScroller(cfg, term_size, **argv)
    colortable = _build_smooth_colortable(DEFAULT_COLOR_TABLE)
    if False:
        use_bold = True
        colortable = _build_smooth_colortable(DEFAULT_COLOR_TABLE_CONSOLE)
    colortable_size = len(colortable)

    print(f"{CLEAR}{HOME}", end="")
    if scroller.line > 0:
        _move_to_line(scroller.line)
    cnt = 0
    offset = 2
    for text in scroller:
        if scroller.line < term_size.get_rows() - 1:
            win_text = text
        else:
            win_text = text[:-1]
        if use_colors:
            win_text = _apply_colors(win_text, cnt, colortable, colortable_size)
        if use_bold:
            win_text = BOLD + win_text
        print(win_text, end="\r")
        if IS_WINDOWS:
            sleep(.15)
        else:
            _check_input(getch)
        cnt += offset
        if _update_term_size(term_size):
            print(f"{CLEAR}{HOME}", end="")
            if scroller.line > 0:
                _move_to_line(scroller.line)
    if IS_WINDOWS:
        print(f"{UP_ONE_ROW}", end="")


def _build_smooth_colortable(color_table):
    colors = color_table
    for pos in range(len(colors) - 1, 0, -1):
        colors.append(color_table[pos])
    return colors


def _apply_colors(win_text, cnt, colortable, colortable_size):
    color_index = cnt % colortable_size
    new_text = ""
    for ch in win_text:
        new_text += f"\033[{colortable[color_index]}" + ch
        color_index += 1
        color_index = color_index % colortable_size
    return new_text


def _check_input(getch):
    """
    Use getchtimeout to get a character. If "Q" or "q" is given, then it raises SystemExit
    """
    character = getch.getch(timeout=.1)
    if isinstance(character, int):
        log.debug("Got key '%d'", character)
    elif isinstance(character, str):
        log.debug("Got key '%s'", character)
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
