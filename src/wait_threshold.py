import time


class WaitThreshold:
    def __init__(self, threshold: float = 0):
        self.threshold = threshold
        self.start_time = time.time()

    def wait(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.threshold:
            time.sleep(self.threshold - elapsed_time)

        self.start_time = time.time()
