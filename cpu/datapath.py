class Datapath:
    
    def __init__(self, mem_file: str) -> None:
        #datapath registers and memory
        self.registers: list[int] = [0] * 16
        self.pc: int = 0    # public
        self.inst: int = 0  # public
        self.memory: list[int] = self._init_memory(mem_file)
        
        #datapath temporary registers for decode
        self.a: int = 0
        self.b: int = 0
        self.imm: int = 0
        self.wb: int = 0 # index of write back register
        self.mdr: int = 0 #memory register
        self.f: int = 0
        
        #return variables for the controller
        self.debug: str | None = None # public 
        self.op: int = 0
        self.zero: bool = False
        self.neg: bool = False
    
    
    def _init_memory(self, mem_file) -> None:
        memory = [0] * 2**16
        
        with open(mem_file, "r") as f:
            while line :=  f.readline():
                line = line.strip()
                if line.startswith('//') or line == "":
                    continue
                
                addr, num = line.split()
                addr = int(addr[1:], 16)
                num = int(num, 16)
                
                memory[addr] = num
        
        return memory
    
    def execute(self, state) -> None:
        state_to_action = {
            "IFETCH": self.fetch,
            "DECODE": self.decode,
            "EX_ADD": lambda: self.alu(0),
            "EX_SUB": lambda: self.alu(1),
            "EX_AND": lambda: self.alu(2),
            "EX_OR": lambda: self.alu(3),
            "EX_NOT": lambda: self.alu(4),
            "EX_SHL": lambda: self.alu(5),
            "EX_SHR": lambda: self.alu(6),
            "EX_LDI": lambda: self.alu(7),
            "EX_LD": lambda: self.alu(8),
            "EX_ST": lambda: self.alu(9),
            "EX_BR": lambda: self.alu(10),
            "EX_BZ": lambda: self.alu(11),
            "EX_BN": lambda: self.alu(11),
            "BR_TAKE": lambda: self.alu(10),
            "BR_NOT": lambda: self.alu(14),
            "EX_JAL": lambda: self.alu(12),
            "EX_JR": lambda: self.alu(13),
            "MEM_LD": self.memory_load,
            "MEM_ST": self.memory_store,
            "WB_ALU": self.alu_writeback,
            "WB_LOAD": self.load_writeback,
            "WB_JAL": self.jal_writeback,
            "EX_QUIT": self.ex_quit
        }
        
        state_to_action[state]()
        return self.op, self.zero, self.neg

    
    def fetch(self) -> None:
        self.inst = self.memory[self.pc]
        self.debug = None
        
    def decode(self) -> None:
        instruction = hex(self.inst)[2:]
        instruction = "0" * (4 - len(instruction)) + instruction
        
        self.op = int(instruction[0], 16)
        
        if self.op <= 6:
            self.wb = int(instruction[1], 16)
            self.a = self.registers[int(instruction[2], 16)]
            self.b = self.registers[int(instruction[3], 16)]
        elif self.op == 7:
            self.wb = int(instruction[1], 16)
            self.imm = int(instruction[2:], 16)
        elif self.op == 8:
            self.wb = int(instruction[1], 16)
            self.imm = int(instruction[2], 16)
            self.b = self.registers[int(instruction[3], 16)]    
        elif self.op == 9:
            self.imm = int(instruction[1], 16)
            self.a = self.registers[int(instruction[2], 16)]
            self.b = self.registers[int(instruction[3], 16)]
        elif self.op == 10:
            self.imm = int(instruction[1:3], 16)
        elif self.op in [11, 12]:
            self.imm = int(instruction[1:3], 16)
            self.b = self.registers[int(instruction[3], 16)]
        elif self.op == 13:
            self.imm = int(instruction[1:], 16)
        elif self.op == 14:
            self.a = self.registers[int(instruction[2], 16)]
        elif self.op == 15:
            pass
        else:   #panic
            print("ERROR: Bad Instuction")
            exit(1)
    
    def ex_quit(self) -> None:
        self.debug = "QUIT"
        exit(0)
    
    
    def memory_load(self) -> None:
        self.mdr = self.memory[self.f]
    
    def memory_store(self) -> None:
        self.memory[self.f] = self.a
        self.pc += 1
        self.debug = f"M[{hex(self.f)[2:]}] = {hex(self.a)} ({self.a})"
    
    def alu_writeback(self) -> None:
        self.registers[self.wb] = self.f
        self.pc += 1
        self.debug = f"r{self.wb} = {hex(self.f)} ({self.f})"
    
    def load_writeback(self) -> None:
        self.registers[self.wb] = self.mdr
        self.pc += 1
        self.debug = f"r{self.wb} = {hex(self.mdr)} ({self.mdr})"
    
    def jal_writeback(self) -> None:
        self.registers[15] = self.f
        self.pc += self.imm
        self.debug = f"r15 = {hex(self.f)} ({self.f})"
        
    def alu(self, op) -> None:
        
        if op == 0: #add
            self.f = self.a + self.b
        elif op == 1: #sub
            self.f = self.a - self.b
        elif op == 2: #and
            self.f = self.a & self.b
        elif op == 3: #or
            self.f = self.a | self.b
        elif op == 4: #not
            self.f = ~self.a
        elif op == 5: #shl
            self.f = self.a << self.b
        elif op == 6: #shr
            self.f = self.a >> self.b
        elif op == 7: #ldi
            self.f = self.imm 
        elif op == 8 or op == 9: #ld and st
            self.f = self.b + self.imm
        elif op == 10: # ex_br | take branch 
            #MIGHT NEED DUBUG HERE
            self.pc += self.imm
        elif op == 11: #ex_bz and ex_bn
            self.zero = self.b == 0
            self.neg = self.b < 0
        elif op == 12: #ex_jal
            self.f = self.pc + 1
        elif op == 13: #ex_jr
             #MIGHT NEED DUBUG HERE
            self.pc = self.a
        elif op == 14: #br not
             #MIGHT NEED DUBUG HERE
            self.pc = self.pc + 1
        else:   #panic
            print("ERROR: Bad Opcode")
            exit(1)
         