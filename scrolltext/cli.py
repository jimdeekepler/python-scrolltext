"""
Main entry point for scrolltext
"""
import sys
from scrolltext import cursesscroller
from scrolltext import linescroller
from scrolltext.utils import init_utils


def main():
    """
    Main method.
    """
    action = _parse_args()
    try:
        cfg = init_utils(False)
        action = action or _str_to_action_type(cfg["main"]["action"])
        action(False)
    except NameError as e:
        print("NameError occured: " + str(e))
        print("Probalby check config?")


def _parse_args():  # pylint: disable=inconsistent-return-statements  (R1710)
    action = None
    for arg in sys.argv[1:]:
        if "cursestext" == arg:
            action = cursesscroller
        elif "linescroller" == arg:
            action = linescroller
    return action


def _str_to_action_type(action):
    if "cursestext" == action:
        action = cursesscroller
    elif "linescroller" == action:
        action = linescroller
    else:
        raise RuntimeError("Unknown 'action' type")
    return action


if __name__ == "__main__":
    main()
