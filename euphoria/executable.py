import signal
import sys

import threading

class Executable:
    """
    A class that can be executed.
    """
    
    def __init__(self):
        pass

    def run(self):
        pass

    def quit(self):
        pass

def start(e):
    """
    Run an exectutable class. This provides a way to make sure that a class is
    properly closed on SIGINT and SIGTERM.
    
    Note: This function should only be called from the main thread.
    """
    
    lock = threading.RLock()
    
    def exit_program(signal, frame):
        with lock:
            e.quit()
            sys.exit()

    signal.signal(signal.SIGTERM, exit_program)
    signal.signal(signal.SIGINT, exit_program)

    e.run()