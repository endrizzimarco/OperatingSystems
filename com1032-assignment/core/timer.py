import time

class Timer:
    def __init__(self):
        self.clock = 1000 #Hz
        self.ticks = 0 # 1 tick = 1ms
        self.initTime = None
        self.quantum = 1
        self.currentQuantum = 0

    def tick(self):
        self.ticks += 1
        self.currentQuantum += 1

    def resetQuantum(self):
        self.currentQuantum = 0

    # used to track the code execution time so that every loop is exactly 1 real millisecond apart
    def setInitTime(self):
        self.initTime = time.time()

    # sleeps 1ms - time it took for previous code to execute
    def sleep(self):
        sleep_ms = (1/self.clock) - (time.time() - self.initTime)
        if sleep_ms > 0:
            time.sleep(sleep_ms) # sleeps exactly 1ms 

