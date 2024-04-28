"""
A simple side scrolling text application.
"""
import shutil
from time import sleep
from .utils import CLEAR, HOME, BOLD, NORMAL, IS_WINDOWS, UP_ONE_ROW, CharacterScroller, TermSize

if not IS_WINDOWS:
    from scrolltext.getchtimeout import GetchWithTimeout


DEFAULT_COLOR_TABLE_GREYSCALE_256 = ["38;5;" + str(x) + "m" for x in range(236, 256)]
DEFAULT_COLOR_TABLE_CONSOLE = [str(x) + "m" for x in [30, 34, 35, 36, 31, 32, 33]]
COLOR_TABLES = [DEFAULT_COLOR_TABLE_GREYSCALE_256, DEFAULT_COLOR_TABLE_CONSOLE]
last_term_rows = -1  # pylint: disable=C0103 (invalid-name)


def linescroller(cfg):
    """
    Main entry point for linescroller.
    :param cfg: Config object
    :type: configparser.ConfigParser
    """
    getch = None
    if not IS_WINDOWS:
        getch = GetchWithTimeout()

    term_size = TermSize(0, 0)
    _update_term_size(term_size)
    try:
        _linescroller(getch, cfg, term_size)
    except RuntimeError:
        pass
    finally:
        if not IS_WINDOWS:
            getch.cleanup()
        else:
            print(f"{UP_ONE_ROW}", end="")


def _linescroller(getch, cfg, term_size):
    """
    Prints a text in a side-scrolling manner.
    """
    argv = {}
    argv["min_scroll_line"] = 0
    scroller = CharacterScroller(cfg, term_size, **argv)
    use_colors = cfg["main"].getboolean("color")
    use_bold = cfg["main"].getboolean("bold")
    colortable = _build_smooth_colortable(cfg)
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
        win_text = _add_ansi_escapes(win_text, cnt, use_bold, use_colors, colortable,
                                     colortable_size)
        print(win_text, end="\r")
        _check_input(getch)
        cnt += offset
        _check_term_resize(scroller, term_size)


def _build_smooth_colortable(cfg):
    color_table_id = cfg["main"].getint("colortable", 0)
    if color_table_id < 0 or color_table_id >= len(COLOR_TABLES):
        color_table_id = 0
    color_table = COLOR_TABLES[color_table_id]
    colors = color_table
    for pos in range(len(colors) - 1, 0, -1):
        colors.append(color_table[pos])
    return colors


# pylint: disable=too-many-arguments (R0913)
def _add_ansi_escapes(win_text, cnt, use_bold, use_colors, colortable, colortable_size):
    if use_colors:
        win_text = _apply_colors(win_text, cnt, colortable, colortable_size)
    if use_bold:
        win_text = BOLD + win_text
    return win_text


def _apply_colors(win_text, cnt, colortable, colortable_size):
    color_index = cnt % colortable_size
    new_text = ""
    for ch in win_text:
        new_text += f"\033[{colortable[color_index]}" + ch
        color_index += 1
        color_index = color_index % colortable_size
    return new_text


def _check_input(getch):
    if IS_WINDOWS:
        sleep(.15)
    else:
        _check_user_keypress(getch)


def _check_user_keypress(getch):
    """
    Use getchtimeout to get a character. If "Q" or "q" is given, then it raises SystemExit
    """
    character = getch.getch(timeout=.1)
    if character is not None and character in ["\033", "\x1b", "", "\r", "", " ", "Q", "q"]:
        print(f"{NORMAL}")
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


def _check_term_resize(scroller, term_size):
    if _update_term_size(term_size):
        print(f"{CLEAR}{HOME}", end="")
        if scroller.line > 0:
            _move_to_line(scroller.line)


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
