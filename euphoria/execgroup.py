from . import executable

import threading
import time

class ExecGroup(executable.Executable):
    """
    A class that groups multiple executables together, so that they can be run
    at the same time.
    """

    def __init__(self, autostop=True, autoclean=True, delay=2):
        super().__init__()

        self.execs = []

        self.autostop = autostop
        self.autoclean = autoclean

        self.delay = delay

    def add(self, toadd):
        """
        add(toadd) -> None

        Add an executable to the list of things to be run.
        """

        self.execs.append(toadd)
        toadd.launch()

    def run(self):
        """
        run() -> None

        Start all the executables and wait in a loop.
        """

        super().run()

        while self.running:
            if self.autostop and len(self.execs) == 0:
                self.quit()

            #Iterate backwards and remove dead threads
            if self.autoclean:
                for i in range(len(self.execs) - 1, -1, -1):
                    if not self.execs[i].running:
                        if self.execs[i].thread is not None:  #Join thread that has not already joined
                            self.execs[i].thread.join()

                        self.execs.remove(self.execs[i])

            time.sleep(self.delay)

    def quit(self):
        for i in self.execs:
            i.quit()

        super().quit()

def bind(*args, autostop=True, autoclean=True):
    """
    bind(*args) -> ExecGroup

    Turn a bunch of executables into a group easily.
    """

    group = ExecGroup(autostop, autoclean)

    for a in args:
        group.add(a)

    return group
