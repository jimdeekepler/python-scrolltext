"""
Utilities for line-based text scrollers.
"""
import sys
from os import getenv
from time import time


CLEAR = "\033[2J"
HOME = "\033[H"
UP_ONE_ROW = "\033[1A"


IS_WINDOWS = sys.platform in ["msys", "win32", "nt"]
DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_DIRECTION = getenv("SCROLL_DIRECTION") or "0"
SCROLL_SPEEDS = [.25, .20, .18, .15, .125, .1, .09, .08, .075, .07, .0675]
SCROLL_TEXT = getenv("SCROLL_TEXT") or DEF_SCROLL_TEXT
SCROLL_LINE_STR = getenv("SCROLL_LINE") or "0"
SCROLL_SPEED = getenv("SCROLL_SPEED") or "0"


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


scroll_direction = parse_int(SCROLL_DIRECTION)
speed_index = parse_int(SCROLL_SPEED)
if speed_index < 0 or speed_index >= len(SCROLL_SPEEDS):
    speed_index = 4  # pylint: disable=C0103  # ignores (invalid-name)
scrollspeedsec = SCROLL_SPEEDS[speed_index]
del speed_index


def get_linenum(min_row, max_row):
    """
    :param min_row: Minimum line number
    :type min_row: int
    :param max_row: Maximum line number
    :type max_row: int
    :returns: int in [min_row, max_row]
    """
    line = min_row
    try:
        line = int(SCROLL_LINE_STR)
    except (TypeError, ValueError):
        pass
    if line < 0:
        line = max_row + line + 1
    line = max(line, min_row)
    line = min(line, max_row)
    return line


class CharacterScroller:  # pylint: disable=R0902  # ignores (too-many-instance-attributes)
    """
    Utility class  for all character based text-scrollers.
    """

    def __init__(self, *args):
        """Objects init method.
        :param args[0]: The number of characters of visible text, e.g. terminal width, number
                        of columns
        :type args[0]: int
        :param args[1]: The number of leading and trailing blank characters to add
        :type args[1]: int
        :param args[2]: The text to scroll
        :type args[2]: str
        :param args[3]: Direction to scroll [0 left-to-right, 1 right-to-left], if missing,
                        left-to-right is used.
        :type args[3]: integer
        :param args[4]: Scrolling Speed in seconds
        :type args[4]: float
        """
        self.visible_text_length = int(args[0])
        self.blanks = int(args[1]) * " "
        self.complete_text = self.blanks + args[2] + self.blanks
        self.pos = 0
        self.terminal_pos = len(self.complete_text)
        if len(args) >= 4:
            self.right_to_left = parse_int(args[3]) == 1
        else:
            self.right_to_left = False
        if len(args) >= 5:
            self.scrollspeedsec = args[4]
        else:
            self.scrollspeedsec = .25
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
        self.last_time = time()
        self._text = self.complete_text

    def __iter__(self):
        return iter(self.next, None)

    def next(self):
        """
        Gives the next visible text to display by the client-program.

        :returns: A str object of visible text length
        :rtype: str
        """
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
            return None
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
            return None
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
