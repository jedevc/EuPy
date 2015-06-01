from . import executable

import threading
import time

class ExecGroup(executable.Executable):
    def __init__(self):
        self.execs = []
        self.exec_threads = []

    def add(self, toadd):
        self.execs.append(toadd)
        self.exec_threads.append(threading.Thread(target=toadd.run))

    def run(self):
        for e in self.exec_threads:
            e.start()

        while len(self.execs) != 0:
            time.sleep(2)

    def quit(self):
        for i in self.execs:
            i.quit()

        for i in self.exec_threads:
            i.join()
        
        self.execs = []
        self.exec_threads = []