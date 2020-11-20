import memory.algorithms as algorithms

class MMU:
    def __init__(self, ram):
        self.ram = ram
        self.frameSize = self.pageSize = 4 * 2**10 # default 8KB
        
        # keep track of all frames and whether they are free, and if not, process and page associated with them
        self.frames = [{'free': True, 'process': None, 'page': None} for _ in range(int(len(self.ram.memory) / self.frameSize))]
        # list containing frames in allocated order 
        self.history = []
        # dict containing all swapped out frames
        self.swap = {}
        # algorithm used to locate next free frame
        self.allocationStrategy = algorithms.FirstFit(self)
        # algorithm used for page swapping
        self.replacementStrategy = algorithms.FIFO(self)

    # returns the page number and offset translated from an address
    def getPageOffset(self, address):
        return int(address / self.pageSize), address % self.pageSize

    # return start and finish of a frame in memory
    def getFrameAddresses(self, frame):
        frameStart = frame * self.frameSize
        return frameStart, (frameStart + self.frameSize)

    # take a swapped out page, swap it back in, and return new index
    def swapIn(self, process, page):
        frame = self.allocatePage(process, page)
        print(f"Swapping in page {self.frames[frame]['page']} from process {self.frames[frame]['process']}")

        (frameStart, frameEnd) = self.getFrameAddresses(frame)
        self.ram.memory[frameStart:frameEnd] = self.swap[process.id][page]
        del self.swap[process.id][page]

        return frame

    # swap out a frame and return index 
    def swapOut(self, process):
        frame = self.replacementStrategy.getExpendableFrame()
        print(f"Swapping out page {self.frames[frame]['page']} from process {self.frames[frame]['process']}")

        page = self.frames[frame]['page']
        process = self.frames[frame]['process']
        (frameStart, frameEnd) = self.getFrameAddresses(frame)

        if not (process in self.swap):
            self.swap[process] = {}

        self.history.remove(frame)
        self.swap[process][page] = self.ram.memory[frameStart:frameEnd]
        return frame

    # returns whether the page is swapped out
    def isSwappedOut(self, process, page):
        return (process.id in self.swap) and (page in self.swap[process.id])

    # allocate a page to physical memory and return corresponding frame
    def allocatePage(self, process, page):
        frame = self.allocationStrategy.getAvailableFrame()
        
        # if memory is full swap out a process
        if frame is None:
            frame = self.swapOut(process)
        
        # update frames list, process' page table
        self.history.append(frame)
        process.pageTable[page] = frame

        self.frames[frame]['free'] = False
        self.frames[frame]['process'] = process.id
        self.frames[frame]['page'] = page

        return frame

    # frees frame and updates page table
    def deallocatePage(self, process, page):
        frame = process.pageTable.get(page)
        if frame is not None:
            self.frames[frame]['free'] = True
            self.frames[frame]['process'] = None
            self.frames[frame]['page'] = None
            del process.pageTable[page]

    # finds physical address corresponding to virtual address and returns it
    def addressLookup(self, process, address):
        (page, offset) = self.getPageOffset(address)
        frame = process.pageTable.get(page)

        # if page is swapped out, swap it back in
        if self.isSwappedOut(process, page):
            frame = self.swapIn(process, page)
        
        # if page fault, allocate page to memory and add to page table
        if frame is None:
            frame = self.allocatePage(process, page)
        
        return frame * self.frameSize + offset
    
    # read a value from memory
    def readMemory(self, process, address):
        return self.ram.memory[self.addressLookup(process, address)]
    
    # write a value to memory
    def writeMemory(self, process, address, value):
        self.ram.memory[self.addressLookup(process, address)] = value

