# NOTE: This is loosely based on: https://github.com/joeyespo/py-getch
"""
Utility for terminal based getch, applying a timeout, when there is no input available.
"""

import select
import sys
import termios
import tty


class GetchWithTimeout:
    """
    This class provides a getch with a timeout.
    """

    def __init__(self):
        """
        Set terminal in rawmode, store original settings for later restore.
        """
        self.fd = sys.stdin.fileno()  # pylint: disable=invalid-name ## C104
        self.old = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)

    def getch(self, timeout: float = .15):
        """
        A getch() with timeout.
        :param timeout: Give a timeout in seconds. This is a float, so you can timeout
                        after 100 milli-seconds with 0.1
        :type timeout: float
        """
        input_array = [sys.stdin]
        ready_tuple = select.select(input_array, [], [], timeout)
        if len(ready_tuple[0]) > 0:
            return ready_tuple[0][0].read(1)
        return None

    def cleanup(self):
        """
        Reset terminal. Call this at program end.
        """
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)
        print()
