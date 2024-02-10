"""
Utilities for line-based text scrollers.
"""


CLEAR = "\033[2J"
HOME = "\033[H"


class CharacterScroller:
    """
    Utility class  for all character based text-scrollers.
    """

    def __init__(self, *args):
        """Objects init method.
        :param args[0]: The number of characters of visible text
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
