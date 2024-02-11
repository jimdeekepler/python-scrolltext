"""
Main entry point for scrolltext
"""
import sys
from scrolltext import cursesscroller
from scrolltext import linescroller


DEF_ACTION = linescroller
action = DEF_ACTION


for arg in sys.argv[1:]:
    if "cursestext" == arg:
        action = cursesscroller


action()
