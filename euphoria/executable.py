import signal
import sys

import time
import datetime

import threading

class Executable:
    """
    A class that can be executed.
    """

    def __init__(self):
        self.running = False
        self.start_time = None
        self.start_utc = datetime.datetime.utcnow()

    def uptime(self):
        return time.time() - self.start_time

    def run(self):
        self.start_time = time.time()
        self.running = True

    def quit(self):
        self.running = False

def start(e):
    """
    Run an exectutable class. This provides a way to make sure that a class is
    properly closed on SIGINT and SIGTERM.

    Note: This function should only be called from the main thread.
    """

    def exit_program(s, f):
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        e.quit()

    signal.signal(signal.SIGTERM, exit_program)
    signal.signal(signal.SIGINT, exit_program)

    e.run()
