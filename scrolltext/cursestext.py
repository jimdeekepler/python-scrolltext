"""
A simple curses-based side scrolling text application.
"""
from curses import wrapper, error
import curses
from .utils import CharacterScroller, IS_WINDOWS, TermSize


NUM_COLORS = 0
QUIT_CHARACTERS = ["\x1B", "Q", "q"]
START_INDEX = 2


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
    if curses.has_colors():
        log.debug("curses has colors %d", curses.COLORS)
        NUM_COLORS = cfg["cursestext"].getint("num_colors", 18)
        NUM_COLORS = min(NUM_COLORS, curses.COLORS - 2)
        _init_colors()
        log.info("using %d colors", curses.COLORS)

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
        if scroller.line >= min_scroll_line:
            _addstr_wrapper(win, scroller.line, (1 if box else 0), win_text)
            win.redrawwin()
        character = get_char(win)
        if character == curses.KEY_EXIT:
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
        log.exception("Error in addstr")
        pass


def _addstr_with_colors_wrapper(win, row, column, text, /, *args):
    global START_INDEX  # pylint: disable=W0603 (global-statement)
    color_index = START_INDEX

    log.debug("addstr to line %d", row)
    try:
        pos = column
        count_up = True
        for character in text:
            win.addstr(row, pos, character, curses.color_pair(color_index), *args)
            log.debug("using color index: %d", color_index)
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
        log.exception("Error in addstr")

    START_INDEX += 1
    if ((START_INDEX - 2) % (2 * NUM_COLORS)) == (2 * NUM_COLORS) - 1:
        START_INDEX = 2
    elif START_INDEX < 2:
        START_INDEX = (2 * NUM_COLORS) - 1


def _check_quit(win, box, term_size, min_scroll_line, scroller):
    character = get_char(win)
    if character == curses.KEY_EXIT:
        return True
    if character == curses.KEY_RESIZE:
        update_term_size(win, box, term_size)
        draw_items(win, box, min_scroll_line, scroller, term_size)
    return False


# pylint: disable=too-many-arguments (R0913)
def _draw_text(win, scroller, term_size, box, win_text, min_scroll_line, term_too_small_printed):
    if scroller.line >= min_scroll_line:
        _addstr_with_colors_wrapper(win, scroller.line, (1 if box else 0), win_text)
        term_too_small_printed = False
        win.redrawwin()
    else:
        if not term_too_small_printed:
            log.debug("Terminal is too small  cols: %d  rows: %d",
                      term_size.get_cols(), term_size.get_rows())
        term_too_small_printed = True
    return term_too_small_printed


def _log_default_color_indexes():
    log.info(curses.COLOR_BLACK)
    log.info(curses.COLOR_RED)
    log.info(curses.COLOR_GREEN)
    log.info(curses.COLOR_YELLOW)
    log.info(curses.COLOR_BLUE)
    log.info(curses.COLOR_MAGENTA)
    log.info(curses.COLOR_CYAN)
    log.info(curses.COLOR_WHITE)
    log.info(curses.color_content(curses.COLOR_YELLOW))


def _init_colors():
    curses.start_color()
    low_color = 280
    color_increase = (1000 - low_color) / NUM_COLORS
    for val in range(2, NUM_COLORS + 2):
        color_value = int(low_color + (val - 2) * color_increase)
        curses.init_color(val, color_value, color_value, color_value)
        curses.init_pair(val, val, curses.COLOR_BLACK)
        log.debug("initialized color index: %d", val)


def work(cfg):
    """Main uses curses.wrapper. See curses doc for details.
    """
    try:  # noqa: C901 ignoring 'TryExcept 42' is too complex - fix later
        wrapper(curses_scroller, cfg)
    except error:
        pass
