class FirstFit:
    def __init__(self, mmu):
        self.mmu = mmu
        self.name = 'FirstFit'

    # return number of next free frame
    def getAvailableFrame(self):
        for index, frame in enumerate(self.mmu.frames):
            if frame['free'] == True:
                return index

class FIFO:
    def __init__(self, mmu):
        self.mmu = mmu
        self.name = 'FIFO'
        
    # return number of next frame to kill
    def getExpendableFrame(self):
        return self.mmu.history[0] if len(self.mmu.history) else None


