from . import executable

import threading
import time

class ExecGroup(executable.Executable):
    """
    A class that groups multiple executables together, so that they can be run
    at the same time.
    """

    def __init__(self, autostop=True):
        self.execs = []
        self.exec_threads = []

        self.lock = threading.Lock()
        self.running = False

        self.autostop = autostop

    def add(self, toadd):
        """
        add(toadd) -> None

        Add an executable to the list of things to be run.
        """

        self.execs.append(toadd)
        th = threading.Thread(target=toadd.run)
        self.exec_threads.append(th)

        with self.lock:
            if self.running:
                th.start()

    def run(self):
        """
        run() -> None

        Start all the executables and wait in a loop.
        """

        with self.lock:
            self.running = True

        for e in self.exec_threads:
            e.start()

        while self.running:
            if self.autostop and len(self.execs) == 0:
                break

            #Iterate backwards and remove dead threads
            for i in range(len(self.execs) - 1, -1, -1):
                if not self.execs[i].running:
                    self.exec_threads[i].join()
                    self.exec_threads.remove(self.exec_threads[i])
                    self.execs.remove(self.execs[i])
            time.sleep(2)

        self.running = False

    def quit(self):
        """
        quit() -> None

        Quit nicely.
        """

        self.running = False

        for i in self.execs:
            i.quit()

        for i in self.exec_threads:
            i.join()
