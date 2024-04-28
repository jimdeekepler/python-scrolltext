"""
Config module for scrolltext
"""
from pathlib import Path
import configparser
import logging
import sys


IS_WINDOWS = sys.platform in ["msys", "win32", "nt"]
DEF_SCROLL_TEXT = """\
Hello, this is a  classic side scrolling text. You can override it by setting the \
environment variable 'SCROLL_TEXT'. It is supposed to be a simple example."""
SCROLL_SPEEDS = [.25, .20, .18, .15, .125, .1, .09, .08, .075, .07, .0675]


log = logging.getLogger(__name__)


initial_config = {
    "main": {"action": "linescroller", "color": 0, "endless": "0"},
    "cursestext": {"box": "1"},
    "scrolltext.text 1": {
        "direction": "0",
        "text": DEF_SCROLL_TEXT,
        "line": "0",
        "speed": "0",
    }
}


def get_speedsec_float(speed_index):
    """
    Get scrollspeedsec from predefined defaults. When index is out of bounds, a default
    speed_index is used.
    :returns: Scroll speed seconds
    :rtype: float
    """
    if speed_index < 0 or speed_index >= len(SCROLL_SPEEDS):
        speed_index = 4
    scrollspeedsec = SCROLL_SPEEDS[speed_index]
    return scrollspeedsec


def init_config(write_config):
    """
    Calls _read_config and sets a default config for missing entries.
    :param write_config: Write initial config
    :type: bool
    """
    if not IS_WINDOWS:
        config_path = Path("~/.config/scrolltextrc").expanduser()
    else:
        config_path = Path("scrolltextrc")

    cfg, really_write = _read_config(config_path)
    if write_config and really_write:
        log.info("Writing a new config '%s' using defaults", config_path)
        _write_config(cfg, config_path)
    return cfg


def _read_config(config_path):
    """
    Reads the config file and returns an object.
    """
    really_write = False
    cfg = configparser.ConfigParser(default_section="main")
    log.debug("try read config path: '%s'", config_path)
    successfully_read_files = cfg.read(config_path)

    if not successfully_read_files:
        really_write = True  # We only write a config file, when it does not already exist.
        log.info("No config file found")
        cfg.update(initial_config)
    else:
        log.debug("config files read: '%s'", successfully_read_files)
    _validate(cfg)
    return cfg, really_write


def _write_config(cfg, config_path):
    with open(config_path, "w", encoding="utf-8") as newfile:
        cfg.write(newfile)


def _validate(cfg):
    """
    Validate config object. NOTE: could be improved
    """
    for section, entries in initial_config.items():
        if "%d" in section:
            section = section.replace("%d", "1")
        if section not in cfg:
            raise NameError("Section '" + section + "' is missing in config")
        _validate_section_entries(cfg, section, entries)

    log.debug(cfg["main"]["action"])

    # NOTE: allow for several "scrolltext.text %d" sections
    # for index in range(2, 9):
    #     scrolltext_section = "scrolltext.text " + str(index)
    #     if not scrolltext_section in cfg:
    #         cfg["main"]["max_index"] = str(index - 1)
    #         log.debug("max scrolltext.text %d", cfg["main"]["max_index"])
    #         break
    _fix_scrolltext_section(cfg, "scrolltext.text 1")
    if "cursestext" not in cfg:
        cfg["cursestext"] = {"box": "1"}
    log.debug("cursestext draw box: %s", cfg["cursestext"].getboolean("box"))


def _validate_section_entries(cfg, section, entries):
    for entry in entries:
        if entry not in cfg[section]:
            raise NameError("Entry '" + entry + "' is missing in Section '"
                            + section + "'")


def _fix_scrolltext_section(cfg, section_name):
    """
    Helper function for joining lines in text to one line.
    """
    text_lines = cfg[section_name]["text"]
    text = "".join(text_lines.split("\n"))
    cfg[section_name]["text"] = text
    log.debug(text)
