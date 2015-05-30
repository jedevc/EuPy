import signal
import sys

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
    
    def exit_program(signal, frame):
        e.quit()
        sys.exit()

    signal.signal(signal.SIGTERM, exit_program)
    signal.signal(signal.SIGINT, exit_program)

    e.run()