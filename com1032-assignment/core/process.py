import random

random.seed(42) # answer to everything
class Process:
    def __init__(self, id, arrivalTime, burstTime, priority):   
        self.id = id
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.priority = priority
        self.runTime = 0
        self.running = False # currently assigned to a cpu
        self.memAddresses = random.sample(list(range(2**20)), 60) #60 KB of random addresses
        self.pageTable = {} # every process can only access its own virtual space 

    def isFinished(self):
        return self.runTime >= self.burstTime
