"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
import curses
from .utils import CharacterScroller, IS_WINDOWS, TermSize


NUM_COLORS = 0
QUIT_CHARACTERS = ["\x1B", "Q", "q"]
START_INDEX = 2
COLOR_UP = True


def curses_scroller(win, cfg):
    """
    Curses-main: render a text in a side-scrolling manner, using curses.

    :param win: Internal curses based object
    :type win: curses._window
    :param cfg: Config object
    :type: configparser.ConfigParser
    """
    global NUM_COLORS  # pylint: disable=W0603 (global-statement)
    if not IS_WINDOWS:
        curses.curs_set(0)  # Hide the cursor
    use_color = cfg["main"].getboolean("color", 0)
    if use_color and curses.has_colors():
        NUM_COLORS = cfg["cursestext"].getint("num_colors", 18)
        NUM_COLORS = min(NUM_COLORS, curses.COLORS - 2)
        if curses.can_change_color():
            _init_colors()

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
    for text in scroller:
        win_text = text
        # hack: When writing to the last line we prevent adding an immediate newline and thus
        #       moving the text upwards, by removing the last character of the visibile text.
        if not box and scroller.line == term_size.get_rows():
            win_text = text[:-1]
        _draw_text(win, cfg, scroller, box, win_text, min_scroll_line)
        if _check_quit(win, box, term_size, min_scroll_line, scroller):
            return


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
    character = None
    character = win.getch(0, 0)
    if character != -1 and (chr(character) in QUIT_CHARACTERS):
        return curses.KEY_EXIT
    return character


def update_term_size(win, box, term_size):
    """
    Updates TermSize object.
    """
    winsize = win.getmaxyx()
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
    try:
        win.addstr(row, column, text)
    except curses.error:
        pass


def _addstr_with_colors_wrapper(win, row, column, text, /, *args):
    global START_INDEX, COLOR_UP  # pylint: disable=W0603 (global-statement)
    color_index = START_INDEX

    try:
        pos = column
        count_up = True
        for character in text:
            win.addstr(row, pos, character, curses.color_pair(color_index), *args)
            pos += 1
            if count_up:
                color_index += 1
                if color_index >= NUM_COLORS - 1:
                    count_up = False
            else:
                color_index -= 1
                if color_index <= 2:
                    count_up = True
    except curses.error:
        pass

    if COLOR_UP:
        START_INDEX += 1
        if START_INDEX == NUM_COLORS + 1:
            COLOR_UP = False
            START_INDEX = NUM_COLORS
    else:
        START_INDEX -= 1
        if START_INDEX == 1:
            COLOR_UP = True
            START_INDEX = 2


def _check_quit(win, box, term_size, min_scroll_line, scroller):
    character = get_char(win)
    if character == curses.KEY_EXIT:
        return True
    if character == curses.KEY_RESIZE:
        update_term_size(win, box, term_size)
        draw_items(win, box, min_scroll_line, scroller, term_size)
    return False


# pylint: disable=too-many-arguments (R0913)
def _draw_text(win, cfg, scroller, box, win_text, min_scroll_line):
    if scroller.line >= min_scroll_line:
        if (cfg["main"].getboolean("color", 0) and
           curses.has_colors() and curses.can_change_color()):
            _addstr_with_colors_wrapper(win, scroller.line, (1 if box else 0), win_text)
        else:
            _addstr_wrapper(win, scroller.line, (1 if box else 0), win_text)
        win.redrawwin()


def _init_colors():
    curses.start_color()
    low_color = 280
    color_increase = (1000 - low_color) / NUM_COLORS
    for val in range(2, NUM_COLORS + 2):
        color_value = int(low_color + (val - 2) * color_increase)
        curses.init_color(val, color_value, color_value, color_value)
        curses.init_pair(val, val, curses.COLOR_BLACK)


def work(cfg):
    """Main uses curses.wrapper. See curses doc for details.
    """
    try:  # noqa: C901 ignoring 'TryExcept 42' is too complex - fix later
        wrapper(curses_scroller, cfg)
    except error:
        pass
