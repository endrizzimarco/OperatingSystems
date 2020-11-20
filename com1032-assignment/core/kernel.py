from random import randint
from scheduling.scheduler import Scheduler
from core.process import Process
from core.timer import Timer
from core.cpu import CPU
from memory.ram import RAM
from scheduling.stats import Stats

class Kernel:
    def __init__(self):
        self.timer = Timer()
        self.scheduler = Scheduler()
        self.memory = RAM()
        self.processes = []
        self.cpus = [CPU(1)]

    # print emulated specs
    def bootUp(self):
        print(f'Total CPU cores: {len(self.cpus)}')
        print(f'Total RAM: {len(self.memory.memory)/2**20} MB')
        print(f'Clock: {self.timer.clock} Hz')
        print(f'Quantum: {self.timer.quantum} ms')
        print(f'Page and frame size: {self.memory.mmu.pageSize/2**10} KB\n')

    # read processes from processes.txt
    def loadProcesses(self):
        try:
            with open('processes.txt', 'r') as f:
                for line in f: 
                    data = line.strip().split(',')
                    self.processes.append(Process(int(data[0]), int(data[1]), int(data[2]), int(data[3])))
        except IOError:
            print("File doesn't exist")
        finally: 
            f.close()
    
    # emulates scheduling and allocation of memory for a processes based on a scheduling algorithm
    def schedulerRun(self):
        stats = Stats()

        while 1:
            self.timer.setInitTime()

            # checks for new processes to add to the ready queue and allocates memory on arrival
            for process in self.processes:
                if process.arrivalTime == self.timer.ticks:
                    self.scheduler.addProcess(process)
                    stats.output(self.timer, process, 'added')
                    for address in process.memAddresses:
                        self.memory.mmu.writeMemory(process, address, randint(0,256))

            # sorts ready queue (non preemptive algorithms only)
            self.scheduler.sortProcesses()

            # simulate multiprocessing by using multiple cpus (if set)
            for cpu in self.cpus:
                try:
                    if cpu.currentProcess == None: # if cpu not running a process fetch the next available one
                        cpu.fetchProcess(self.scheduler.getAvailableProcess())
                        stats.output(self.timer, cpu.currentProcess, 'working', cpu.id)
                    else: cpu.runProcess() # else if already assigned a process increase its runtime
                except IndexError: # if ready queue empty go to next cpu
                    continue
                
                # handles finished process 
                if cpu.currentProcess.isFinished():
                    stats.turnaroundTimes.append(self.timer.ticks - cpu.currentProcess.arrivalTime)
                    stats.waitingTimes.append(stats.turnaroundTimes[-1] - cpu.currentProcess.burstTime)
                    stats.output(self.timer, cpu.currentProcess, 'finished')

                    # deallocate process' pages, remove process from cpu and readyqueue
                    for page in list(cpu.currentProcess.pageTable):
                        self.memory.mmu.deallocatePage(cpu.currentProcess, page)
                    self.scheduler.removeProcess(cpu.currentProcess)
                    cpu.freeCPU()
                    
                    # fetch next process
                    try:
                        self.scheduler.sortProcesses()
                        cpu.fetchProcess(self.scheduler.getAvailableProcess())
                        stats.output(self.timer, cpu.currentProcess, 'working', cpu.id)
                        self.timer.resetQuantum()
                    except IndexError: # if ready queue is empty go to next cpu
                        continue
                
                # handles a process time slice running out for preemptive algorithms
                # frees the cpu and releases the process, reorders the ready queue and fetches the next available process
                if (self.scheduler.strategy.name == 'RR' and self.timer.currentQuantum == self.timer.quantum):
                    cpu.freeCPU()
                    self.scheduler.strategy.sortProcesses()
                    cpu.fetchProcess(self.scheduler.getAvailableProcess())
                    stats.output(self.timer, cpu.currentProcess, 'working', cpu.id)
                    self.timer.resetQuantum()

                # handles process accessing cpu for the first time
                if (cpu.currentProcess.runTime == 0):
                    stats.responseTimes.append(self.timer.ticks - cpu.currentProcess.arrivalTime)
                    stats.output(self.timer, cpu.currentProcess, 'accessed')
            
            # when all cpu are finished, go to next millisecond
            self.timer.sleep()
            self.timer.tick()

            # when ready queue is empty end the simulation
            if(len(self.scheduler.readyQueue) == 0):
                break

        results = stats.finalStats()

        print('\n' + stats.finalStats() + '\n')
        self.varReset()
        
        return results

    # reset variables every simulation
    def varReset(self):
        self.processes = []
        self.timer.ticks=self.timer.currentQuantum = 0
        self.memory.mmu.swap = {}
        self.memory.mmu.history = []

    # set number of cores to use for simulation
    def setCpus(self, n):
        self.cpus = []
        for i in range(1, n+1):
            self.cpus.append(CPU(i))
