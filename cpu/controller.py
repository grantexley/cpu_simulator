
class Controller:
    
    def __init__(self) -> None:
        self.state = "IFETCH"
    
    def update_state(self, op, zero, neg) -> None:
        ex_ops = {
            0: "EX_ADD",
            1: "EX_SUB",
            2: "EX_AND",
            3: "EX_OR",
            4: "EX_NOT",
            5: "EX_SHL",
            6: "EX_SHR",
            7: "EX_LDI",
            8: "EX_LD",
            9: "EX_ST",
            10: "EX_BR",
            11: "EX_BZ",
            12: "EX_BN",
            13: "EX_JAL",
            14: "EX_JR",
            15: "EX_QUIT"
        }
        
        def bz_decision(zero):
            if zero:
                return "BR_TAKE"
            else:
                return "BR_NOT"
            
        def bn_decision(neg):
            if neg:
                return "BR_TAKE"
            else:
                return "BR_NOT"
        
        next_state = {
            "IFETCH": "DECODE",
            "DECODE": ex_ops[op],
            "EX_ADD": "WB_ALU",
            "EX_SUB": "WB_ALU",
            "EX_AND": "WB_ALU",
            "EX_OR": "WB_ALU",
            "EX_NOT": "WB_ALU",
            "EX_SHL": "WB_ALU",
            "EX_SHR": "WB_ALU",
            "EX_LDI": "WB_ALU",
            "EX_LD": "MEM_LD",
            "EX_ST": "MEM_ST",
            "EX_BR": "IFETCH",
            "EX_BZ": bz_decision(zero),
            "EX_BN": bn_decision(neg),
            "EX_JAL": "WB_JAL",
            "EX_JR": "IFETCH",
            "EX_QUIT": "EX_QUIT",
            "MEM_LD": "WB_LD",
            "MEM_ST": "IFETCH",
            "WB_ALU": "IFETCH",
            "WB_LD": "IFETCH",
            "WB_JAL": "IFETCH",
            "BR_TAKE": "IFETCH",
            "BR_NOT": "IFETCH"
        }
        
        self.state = next_state[self.state]