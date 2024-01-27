"""
A simple side scrolling text application.
"""
from os import getenv
from time import sleep
from utils import CharacterScroller


DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_TEXT = getenv("SCROLL_TEXT") or DEF_SCROLL_TEXT
VISIBILE_TEXT_LENGTH = 80


def linescroller():
    """
    Prints a text in a side-scrolling manner.
    """
    scroller = CharacterScroller(VISIBILE_TEXT_LENGTH, VISIBILE_TEXT_LENGTH, SCROLL_TEXT)
    for text in scroller:
        win_text = text
        print(win_text, end="\r")
        sleep(.15)


if __name__ == "__main__":
    linescroller()
