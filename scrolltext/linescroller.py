"""
A simple side scrolling text application.
"""
from os import getenv
from time import sleep


DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_TEXT = getenv("SCROLL_TEXT") or DEF_SCROLL_TEXT
VISIBILE_TEXT_LENGTH = 80


def linescroller():
    """
    Prints a text in a side-scrolling manner.
    """
    blanks = " " * VISIBILE_TEXT_LENGTH
    complete_text = blanks + SCROLL_TEXT + blanks
    for start in range(len(complete_text)):
        end = start + VISIBILE_TEXT_LENGTH
        win_text = complete_text[start:end]
        print(win_text, end="\r")
        sleep(.15)
        start += 1


if __name__ == "__main__":
    linescroller()
