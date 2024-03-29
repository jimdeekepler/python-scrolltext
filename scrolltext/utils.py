"""
Utilities for line-based text scrollers.
"""
import logging
from os import getenv
from time import time
from scrolltext.config import get_speedsec_float, init_config
from scrolltext.config import IS_WINDOWS  # pylint: disable=no-name-in-module (W0611)


CLEAR = "\033[2J"
HOME = "\033[H"
UP_ONE_ROW = "\033[1A"


log = logging.getLogger(__name__)


def parse_int(var):
    """
    Calls int on var, ignores TypeError and ValueError.

    :returns: Integer value given in var string, 0 if one of the forementioned errors occurs.
    :rtype: int
    """
    try:
        value = int(var)
        return value
    except (TypeError, ValueError):
        pass
    return 0


def init_utils(write_config):
    """
    Initialises config object and updates some configs via environment varialbes, if
    set.
    :param write_config: Write initial config
    :type: bool
    """
    cfg = init_config(write_config)
    _override_from_env(cfg)
    _init_logging(cfg)
    return cfg


def get_linenum(scroll_line_str, min_row, max_row):
    """
    :param scroll_line_str: Terminal line number for one scrolling text
    :type scroll_line_str: str
    :param min_row: Minimum line number
    :type min_row: int
    :param max_row: Maximum line number
    :type max_row: int
    :returns: int in [min_row, max_row]
    """
    line = min_row
    try:
        line = int(scroll_line_str)
    except (TypeError, ValueError):
        pass
    if line < 0:
        line = max_row + line + 1
    line = max(line, min_row)
    line = min(line, max_row)
    log.debug("scroll_line_str: %s  min: %d  max: %d  line:%d",
              scroll_line_str, min_row, max_row, line)
    return line


def _init_logging(cfg):
    verbose = cfg["main"].getboolean("verbose")
    if verbose:
        # logging.basicConfig(filename="cursesscroller.log", filemode="w", level=logging.DEBUG)
        logging.basicConfig(filename="scrolltext.log", filemode="w", level=logging.DEBUG)


def _override_from_env(cfg):
    _override_verbose(cfg)  # x x x  todo: recap (all of those ...)
    _override_scroll_box(cfg)
    _override_scroll_direction(cfg)
    _override_scroll_text(cfg)
    _override_scroll_line(cfg)
    _override_scroll_speed(cfg)


def _override_verbose(cfg):
    verbose = getenv("VERBOSE") == "1"
    if verbose:
        log.debug("Using env-var 'VERBOSE'")
        cfg["main"]["verbose"] = "1"


def _override_scroll_box(cfg):
    scroll_direction = getenv("SCROLL_BOX") == "1"
    if scroll_direction:
        log.debug("Using env-var 'SCROLL_BOX'")
        cfg["cursestext"]["box"] = "1"


def _override_scroll_direction(cfg):
    scroll_direction = getenv("SCROLL_DIRECTION") == "1"
    if scroll_direction:
        log.debug("Using env-var 'SCROLL_DIRECTION'")
        cfg["scrolltext.text 1"]["direction"] = "1"


def _override_scroll_text(cfg):
    scroll_text = getenv("SCROLL_TEXT")
    if scroll_text:
        log.debug("Using env-var 'SCROLL_TEXT'")
        cfg["scrolltext.text 1"]["text"] = scroll_text


def _override_scroll_line(cfg):
    scroll_line_str = getenv("SCROLL_LINE")
    if scroll_line_str:
        log.debug("Using env-var 'SCROLL_LINE_STR'")
        cfg["scrolltext.text 1"]["line"] = scroll_line_str


def _override_scroll_speed(cfg):
    scroll_speed = getenv("SCROLL_SPEED")
    if scroll_speed:
        scroll_speed_index = parse_int(getenv("SCROLL_SPEED"))
        log.debug("Using env-var 'SCROLL_SPEED' with '%s'", scroll_speed)
        cfg["scrolltext.text 1"]["speed"] = str(scroll_speed_index)


class TermSize:
    """
    Stores terminal columns and rows
    """
    def __init__(self, cols, rows):
        """
        Initializes current terminal size
        :param cols: Current terminal columns
        :ptype cols: int
        :param rows: Current terminal rows
        :ptype rows: int
        """
        self.term_columns = cols
        self.term_rows = rows
        self.resized = False

    def set_size(self, cols, rows):
        """
        Checks if the terminal window size has changed, and sets the
        new term columns and rows paramters. Also sets the resized flag.
        """
        if self.term_columns != cols:
            self.term_columns = cols
            self.resized = True
        if self.term_rows != rows:
            self.term_rows = rows
            self.resized = True
        if self.resized:
            log.debug("TermSize  columns: %d  rows: %d", self.term_columns, self.term_rows)

    def is_resized(self):
        """
        Returns true, when the terminal window changed its size.
        """
        resized = self.resized
        self.resized = False
        if resized:
            log.debug("TermSize resized")
        return resized

    def get_cols(self):
        """ Return terminal columns. """
        return self.term_columns

    def get_rows(self):
        """ Return terminal rows. """
        return self.term_rows


class CharacterScroller:  # pylint: disable=R0902  # disable (too-many-instance-attributes)
    """
    Utility class  for all character based text-scrollers.
    """

    def __init__(self, cfg, term_size, **argv):
        """Objects init method.
        :param cfg: Configuration dictionary
        :type: configparser.ConfigParser
        :param term_size: Current terminal size, number of available columns and rows
        :type: TermSize
        :param argv["section_index"]: Number of scrolltext.text section in use [1..3]
        :param argv["term_rows"]: Terminal height in number of rows
        :param argv["term_columns"]: Terminal width in number of columns
        :param argv["min_scroll_line"]: The minimum terminal row allowed
        :param argv["test"]: Only used in unittests
        """
        self.term_size = term_size
        self.visible_text_length = self.term_size.get_cols()
        log.debug("visibile_text_length: %d", self.visible_text_length)
        self.min_scroll_line = argv["min_scroll_line"] if "min_scroll_line" in argv else 0
        self.endless = cfg["main"].getboolean("endless")

        section_index = str(argv["section_index"]) if "section_index" in argv else "1"
        str_section = "scrolltext.text " + section_index
        scroll_text = cfg[str_section]["text"]
        self.scroll_line_str = cfg[str_section]["line"]
        scroll_direction = cfg[str_section].getboolean("direction")

        self._resized()

        num_blanks = argv["blanks"] if "blanks" in argv else self.visible_text_length
        self.blanks = num_blanks * " "
        self.complete_text = self.blanks + scroll_text + (self.blanks if not self.endless else "")
        self.pos = 0
        self._last_pos = 0
        self.terminal_pos = len(self.complete_text)
        self.right_to_left = scroll_direction
        if "test" in argv:
            self.scrollspeedsec = 0
        else:
            self.scrollspeedsec = get_speedsec_float(cfg[str_section].getint("speed"))
        self._set_start_params()
        self.last_time = time()
        self._text = self.complete_text

    def __iter__(self):
        return iter(self.next, None)

    def _resized(self):
        self.line = get_linenum(self.scroll_line_str,
                                self.min_scroll_line, self.term_size.get_rows())
        self.visible_text_length = self.term_size.get_cols()
        log.debug("_resized  line: %d  columnns: %d  rows: %d  text-length %d",
                  self.line, self.term_size.get_cols(),
                  self.term_size.get_rows(), self.visible_text_length)

    def next(self):
        """
        Gives the next visible text to display by the client-program.

        :returns: A str object of visible text length
        :rtype: str
        """
        if self.term_size.is_resized():
            self._resized()
        if not self.right_to_left:
            return self._next_left_to_right()
        return self._next_right_to_left()

    def _next_left_to_right(self):
        """
        Gives the next visible text to display by the client-program.
        Left-to-right reading text

        :returns: A str object of visible text length
        :rtype: str
        """
        if self.pos >= self.terminal_pos:
            if not self.endless:
                return None
            self._set_start_params()
        end = self.pos + self.visible_text_length
        win_text = self.complete_text[self.pos:end]
        if self.scrollspeedsec == 0:  # Special case for tests
            self.pos += 1
            return win_text
        time_now = time()
        delta = time_now - self.last_time
        self.last_time = time_now
        offset = delta / self.scrollspeedsec
        self._pos_real += offset
        if int(self._pos_real) != self._last_pos:
            self.pos = int(self._pos_real)
            self._last_pos = self.pos
        self._text = win_text
        return self._text

    def _next_right_to_left(self):
        """
        Gives the next visible text to display by the client-program.
        Right-to-left reading text

        :returns: A str object of visible text length
        :rtype: str
        """
        if self.pos <= self.terminal_pos:
            if not self.endless:
                return None
            self._set_start_params()
        start = self.pos - self.visible_text_length
        win_text = self.complete_text[start:self.pos]
        if self.scrollspeedsec == 0:  # Special case for tests
            self.pos -= 1
            return win_text
        time_now = time()
        delta = time_now - self.last_time
        self.last_time = time_now
        offset = delta / self.scrollspeedsec
        self._pos_real -= offset
        if int(self._pos_real) != self._last_pos:
            self.pos = int(self._pos_real)
            self._last_pos = self.pos
        self._text = win_text
        return self._text

    def _set_start_params(self):
        if not self.right_to_left:
            self.pos = 0
            self.terminal_pos = len(self.complete_text)
            self._pos_real = 0.
            self._last_pos = 0
        else:
            self.pos = len(self.complete_text)
            self.terminal_pos = -1
            self._pos_real = float(self.pos)
            self._last_pos = self.pos
