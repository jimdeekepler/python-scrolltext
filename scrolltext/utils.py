"""
Utilities for line-based text scrollers.
"""
class CharacterScroller:
    """
    Utility class  for all character based text-scroller applications.
    """

    def __init__(self, *args, **argv):
        """
        ob das klappt???
        
        args[0] : int -> number of characters of visible text 
        args[1] : int -> number of leading and trailing blank characters to add
        args[2] : str -> the text to scroll 

        """
        self.visible_text_length = int(args[0])
        self.blanks = int(args[1]) * " "
        self.complete_text = self.blanks + args[2] + self.blanks
        self.pos = 0
        self.terminal_pos = len(self.complete_text)

    def __iter__(self):
        return iter(self._next, None)

    def _next(self):
        if self.pos == self.terminal_pos:
            return None
        end = self.pos + self.visible_text_length
        win_text = self.complete_text[self.pos:end]
        self.pos += 1
        return win_text
