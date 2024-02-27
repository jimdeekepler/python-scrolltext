"""
Utilities for line-based text scrollers.
"""
from os import getenv


CLEAR = "\033[2J"
HOME = "\033[H"


DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_TEXT = getenv("SCROLL_TEXT") or DEF_SCROLL_TEXT
SCROLL_LINE_STR = getenv("SCROLL_LINE") or "0"


def parse_int(var):
    """
    Calls int on var, ignores TypeError and ValueError.

    :returns: Integer value given in var string, 0 if one of the forementioned errors occurs.
    """
    try:
        value = int(var)
        return value
    except (TypeError, ValueError):
        pass
    return value


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
        line = max_row + line
    elif line > 0:
        line -= 1
    if line < min_row:
        line = min_row
    if line > max_row:
        line = max_row
    return line


class CharacterScroller:
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
        """
        self.visible_text_length = int(args[0])
        self.blanks = int(args[1]) * " "
        self.complete_text = self.blanks + args[2] + self.blanks
        self.pos = 0
        self.terminal_pos = len(self.complete_text)

    def __iter__(self):
        return iter(self.next, None)

    def next(self):
        """
        Gives the next visible text to display by the client-program.

        :returns: A str object of visible text length
        :rtype: str
        """
        if self.pos == self.terminal_pos:
            return None
        end = self.pos + self.visible_text_length
        win_text = self.complete_text[self.pos:end]
        self.pos += 1
        return win_text
