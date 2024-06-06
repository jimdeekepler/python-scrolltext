"""
Utilities for line-based text scrollers.
"""
import sys
from os import getenv
from time import time
from scrolltext.config import get_speedsec_float, init_config
from scrolltext.config import IS_WINDOWS  # pylint: disable=no-name-in-module (W0611)


EARLY_VERBOSE = getenv("VERBOSE")
CLEAR = "\033[2J"
HOME = "\033[H"
BOLD = "\033[1m"
NORMAL = "\033[0m"
UP_ONE_ROW = "\033[1A"


def parse_int(var):
    """
    Calls int on var, ignores TypeError and ValueError.

    :returns: Integer value given in var string, 0 if one of the aforementioned errors occurs.
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
    Initialises config object and updates some configurations via environment variables, if
    set.
    :param write_config: Write initial config
    :type: bool
    """
    cfg = init_config(write_config)
    _override_from_env(cfg)
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
    return line


def _override_from_env(cfg):
    _override_verbose(cfg)
    _override_scroll_box(cfg)
    _override_scroll_direction(cfg)
    _override_scroll_text(cfg)
    _override_scroll_line(cfg)
    _override_scroll_speed(cfg)


def _override_verbose(cfg):
    _check_and_override_boolean_var(cfg, "VERBOSE", ["main", "verbose"])


def _override_scroll_box(cfg):
    _check_and_override_boolean_var(cfg, "SCROLL_BOX", ["cursestext", "box"])


def _override_scroll_direction(cfg):
    scroll_direction = getenv("SCROLL_DIRECTION") == "1"
    if scroll_direction:
        cfg["scrolltext.text 1"]["direction"] = "1"


def _override_scroll_text(cfg):
    scroll_text = getenv("SCROLL_TEXT")
    if scroll_text:
        cfg["scrolltext.text 1"]["text"] = scroll_text


def _override_scroll_line(cfg):
    scroll_line_str = getenv("SCROLL_LINE")
    if scroll_line_str:
        if EARLY_VERBOSE:
            print("Using env-var 'SCROLL_LINE_STR'", file=sys.stderr)
        cfg["scrolltext.text 1"]["line"] = scroll_line_str


def _override_scroll_speed(cfg):
    scroll_speed = getenv("SCROLL_SPEED")
    if scroll_speed:
        scroll_speed_index = parse_int(getenv("SCROLL_SPEED"))
        if EARLY_VERBOSE:
            # pylint: disable=C0209  (consider-using-f-string)
            print("Using env-var 'SCROLL_SPEED' with '{}'".format(scroll_speed), file=sys.stderr)
        cfg["scrolltext.text 1"]["speed"] = str(scroll_speed_index)


def _check_and_override_boolean_var(cfg, var_name, *args):
    env_value = getenv(var_name)
    if env_value is None:
        return
    if len(*args) < 2:
        raise RuntimeError("Need  2 args in _check_and_override_boolean_var.")

    section, option = args[0][0], args[0][1]
    if env_value == "1":
        if EARLY_VERBOSE:
            # pylint: disable=C0209  (consider-using-f-string)
            print("Using env-var '{}' = {}".format(var_name, env_value), file=sys.stderr)
        cfg.set(section, option, "1")
    else:
        if EARLY_VERBOSE:
            # pylint: disable=C0209  (consider-using-f-string)
            print("Assuming env-var '{}'={} is False".format(var_name, env_value), file=sys.stderr)
        cfg.set(section, option, "0")


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
        new term columns and rows parameters. Also sets the resized flag.
        """
        if self.term_columns != cols:
            self.term_columns = cols
            self.resized = True
        if self.term_rows != rows:
            self.term_rows = rows
            self.resized = True

    def is_resized(self):
        """
        Returns true, when the terminal window changed its size.
        """
        resized = self.resized
        self.resized = False
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
        :param argv["min_scroll_line"]: The minimum terminal row allowed
        :param argv["test"]: Only used in unit tests
        """
        self.term_size = term_size
        self.min_scroll_line = argv["min_scroll_line"] if "min_scroll_line" in argv else 0
        self.endless = cfg["main"].getboolean("endless")

        section_index = str(argv["section_index"]) if "section_index" in argv else "1"
        str_section = "scrolltext.text " + section_index
        self.scroll_text = cfg[str_section]["text"]
        self.scroll_line_str = cfg[str_section]["line"]
        scroll_direction = cfg[str_section].getboolean("direction")

        self.visible_text_length = -1
        self._resized(**argv)

        self._update_complete_text()
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

    def _resized(self, **argv):
        self.line = get_linenum(self.scroll_line_str,
                                self.min_scroll_line, self.term_size.get_rows())
        if self.term_size.get_cols() != self.visible_text_length:
            self.visible_text_length = self.term_size.get_cols()
            self.num_blanks = argv["blanks"] if "blanks" in argv else self.visible_text_length
            self._update_complete_text()

    def _update_complete_text(self):
        blanks = self.num_blanks * " "
        self.complete_text = blanks + self.scroll_text + (blanks if not self.endless else "    ")

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
