


class Datapath:
    
    def __init__(self, mem_file: str) -> None:
        self.registers: list[int] = [0] * 16
        self.pc: int = 0
        self.inst: int = 0
        self.memory: list[int] = self._init_memory(mem_file)
        self.a: int = 0
        self.b: int = 0
        self.wb: int = 0 # write back register
        self.mdr: int = 0 #memory register
        self.f: int = 0
    
    
    
    def _init_memory(self, mem_file) -> None:
        memory = [0] * 2**16
        
        #TODO
        
        return memory
    
    
    def fetch(self) -> int:
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction
    
        
    def decode(self) -> None:
        pass
    
    
    def execute(self) -> None:
        pass
    
    
    
    def alu(self, op) -> None:
        
        
    
