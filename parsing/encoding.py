OPCODES = {
    "add": "0",
    "sub": "1",
    "and": "2",
    "or" : "3",
    "not": "4",
    "shl": "5",
    "shr": "6",
    "ldi": "7",
    "ld" : "8",
    "st" : "9",
    "br" : "A",
    "bz" : "B",
    "bn" : "C",
    "jal": "D",
    "jr" : "E",
    "quit": "F",
}



def encode_instruction(op: str, params: list[str]) -> str | None:
    print('     OP:', op)
    print('     PARAMS', params)
    
    return 'temp'