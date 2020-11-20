class CPU:
    def __init__(self, id):
        self.id = id
        self.currentProcess = None

    def runProcess(self):
        self.currentProcess.runTime += 1

    def fetchProcess(self, process):
        self.currentProcess = process
        self.currentProcess.running = True

    def freeCPU(self):     
        self.currentProcess.running = False
        self.currentProcess = None





