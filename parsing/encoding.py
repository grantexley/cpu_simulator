    
def register_to_num(reg: str):
    if not reg.startswith("r"):
        raise SyntaxError("registers must be r[0-15]")

    try:    
        result = hex(int(reg[1:]))[2:].upper()
        assert len(result) == 1
        return result
    except:
        raise SyntaxError("registers must be r[0-15]")
    
def convert_all_registers(params: list[str]):
    result = ""
    
    for reg in params:
        result += register_to_num(reg)
        
    return result
    

def add(params: list[str]):
    return "0" + convert_all_registers(params)


def sub(params: list[str]):
    return "1" + convert_all_registers(params)

def and_(params: list[str]):
    return "2" + convert_all_registers(params)

def or_(params: list[str]):
    return "3" + convert_all_registers(params)

def not_(params: list[str]):
    return "4" + convert_all_registers(params) + "0"

def shl(params: list[str]):
    return "5" + convert_all_registers(params)

def shr(params: list[str]):
    return "6" + convert_all_registers(params)

def ldi(params: list[str]):
    return "7" + register_to_num(params[0]) + "0" * (2 - len(params[1])) + params[1]

def ld(params: list[str]):
    return "8" + register_to_num(params[0]) + params[2] + register_to_num(params[1])

def st(params: list[str]):
    return "9" + params[2] + convert_all_registers(params[:2])

def br(params: list[str]):
    return "A" + "0" * (2 - len(params[0])) + params[0] + "0"

def bz(params: list[str]):
    return "B" + "0" * (2 - len(params[1])) + params[1] + register_to_num(params[0])

def bn(params: list[str]):
    return "C" + "0" * (2 - len(params[1])) + params[1] + register_to_num(params[0])

def jal(params: list[str]):
    return "D" + "0" * (3 - len(params[0])) + params[0]
def jr(params: list[str]):
    return "E0" + register_to_num(params[0]) + "0"

OPCODES = {
    "add": add,
    "sub": sub,
    "and": and_,
    "or" : or_,
    "not": not_,
    "shl": shl,
    "shr": shr,
    "ldi": ldi,
    "ld" : ld,
    "st" : st,
    "br" : br,
    "bz" : bz,
    "bn" : bn,
    "jal": jal,
    "jr" : jr
}


def encode_instruction(op: str, params: list[str]) -> str :
    
    if op not in OPCODES:
        raise SyntaxError("Invalid Operation")
    
    try:
        result = OPCODES[op](params)
        if not result:
            result = "nope"
        assert(len(result) == 4)
        return result
    except Exception as e:
        raise SyntaxError(f"An error occurered parsing the line")