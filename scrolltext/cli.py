"""
Main entry point for scrolltext
"""
import sys
from scrolltext import cursesscroller
from scrolltext import linescroller
from scrolltext.utils import init_utils


HELP = """\
scrolltext [-w|--write] action

    -w|--write  write initial config

    action      cursestext or linescroller

"""
VERSION = "scrolltext v0.0.11"  # possible improvement: use importlib metadata?


def main():
    """
    Main method.
    """
    write_config, action = _parse_args()
    try:
        cfg = init_utils(write_config)
        action = action or _str_to_action_type(cfg["main"]["action"])
        action(cfg)
    except KeyError as e:
        print("KeyError occurred: " + str(e) + "\nYou probably want to update 'scrolltextrc'.")
    except NameError as e:
        print("NameError occurred: " + str(e) + "\nYou probably want to update 'scrolltextrc'.")


def _parse_args():  # pylint: disable=inconsistent-return-statements  (R1710)
    write_config = False
    action = None
    for arg in sys.argv[1:]:
        if _check_help_or_version(arg):
            sys.exit(0)

        if arg in ["-w", "--write"]:
            write_config = True
        elif "cursestext" == arg:
            action = cursesscroller
        elif "linescroller" == arg:
            action = linescroller
    return write_config, action


def _check_help_or_version(arg):
    if arg in ["-h", "--help"]:
        print(HELP)
        return True
    if arg in ["-v", "--version"]:
        print(VERSION)
        return True
    return False


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
