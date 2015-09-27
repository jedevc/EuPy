import time

from . import executable

class ForeverCall(executable.Executable):
    """
    Call a function forever with a delay.
    """

    def __init__(self, callback, delay, wait=3):
        super().__init__()

        self.callback = callback
        self.delay = delay
        self.wait = wait

        self.last_call = None

    def reset(self):
        self.last_call = time.time()

    def run(self):
        super().run()

        self.last_call = time.time()
        while self.running:
            if self.delay is not None:
                if time.time() - self.last_call >= self.delay:
                    self.callback()
                    self.reset()

            time.sleep(self.wait)
