import random
from memory.mmu import MMU

class RAM:
    def __init__(self):
        self.memory = [0 for x in range(0, 2**20)] # default 1 MB
        self.mmu = MMU(self)

    # set memory size to n kilobytes
    def setMemory(self, n):
        self.memory = [0 for x in range(0, n * 2**20)]

    # show memory from byte x to byte y
    def showMemory(self, x, y):
        print(self.memory[x:y])

