"""
Main entry point for scrolltext
"""
import sys
from scrolltext import cursesscroller
from scrolltext import linescroller


def main():
    invoke = linescroller
    for arg in sys.argv[1:]:
        if "cursestext" == arg:
            invoke = cursesscroller

    invoke()
