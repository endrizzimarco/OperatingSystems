import traceback

class Commands:
    def __init__(self, kernel):
        self.k = kernel

    # print hardware specifications
    def specs(self, args):
        self.k.bootUp()
    
    # run simulation
    def scheduler(self, args):
        try: 
            self.k.loadProcesses()
            self.k.schedulerRun()
        except Exception:
            traceback.print_exc()

    # set scheduler algorithm
    def setScheduler(self, args):
        if self.k.scheduler.setAlgorithm(args[0]):
            print("Invalid input: please choose between RR, FCFS, SJF, Priority") 

    # print current scheduler's algorithm name
    def schedulerName(self, args):
        print(self.k.scheduler.strategy.name)

    # set cpu number to use in simulation
    def setCores(self, args):
        try:
            if(int(args[0])) > 0:
                self.k.setCpus(int(args[0]))
            else:
                print('Please insert a positive number')
        except:
            print('Please insert a valid number')

    # set time slice to use in simulation
    def setQuantum(self, args):
        try:
            if(int(args[0])) > 0:
                self.k.timer.quantum = int(args[0])
            else:
                print('Please insert a positive number')
        except:
            print('Please insert a valid number')

    # set memory size 
    def setMemory(self, args):
        try:
            if(int(args[0])) > 0:
                self.k.memory.setMemory(int(args[0]))
                self.k.memory.mmu.frames = [{'free': True, 'process': None, 'page': None} for _ in range(int(len(self.k.memory.memory) / self.k.memory.mmu.frameSize))]

            else:
                print('Please insert a positive number')
        except:
            print('Please insert a valid number')

    # set frame and page size
    def setFrameSize(self, args):
        try:
            if(int(args[0])) > 0:
                self.k.memory.mmu.frameSize = int(args[0]) * 2**10
                self.k.memory.mmu.pageSize = int(args[0]) * 2**10
                self.k.memory.mmu.frames = [{'free': True, 'process': None, 'page': None} for _ in range(int(len(self.k.memory.memory) / self.k.memory.mmu.frameSize))]
            else:
                print('Please insert a positive number')
        except:
            traceback.print_exc()
    # print segment of memory
    def showMemory(self, args):
        try:
            if(int(args[0]) or int(args[1]) ) > 0:
                if(int(args[0]) < int(args[1])):
                    self.k.memory.showMemory(int(args[0]), int(args[1]))
                else:
                    print('Second input must be bigger than first')
            else:
                print('Please insert positive numbers')
        except:
            print('Please insert a valid number')



