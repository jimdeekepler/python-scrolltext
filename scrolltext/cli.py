"""
Main entry point for scrolltext
"""
import sys
from scrolltext import cursesscroller
from scrolltext import linescroller


def main():
    """
    Main method.
    """
    invoke = linescroller
    for arg in sys.argv[1:]:
        if "cursestext" == arg:
            invoke = cursesscroller

    invoke()


if __name__ == "__main__":
    main()
