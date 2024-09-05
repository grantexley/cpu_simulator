#!/usr/bin/env python3
from encoding import encode_instruction
import sys
import os
from dataclasses import dataclass
from enum import Enum


class Directive(Enum):
    text = "text"
    data = "data"

@dataclass
class Instruction:
    line: str
    line_num: int
    
def parse_data_segment(instructions: list[Instruction], start_index: int) -> tuple[list[str], dict]:
    
    target_lookup = {}
    data_lines = []
    
    for i, inst in enumerate(instructions):
        
        if ":" not in inst.line:
            print(f"LINE {inst.line_num} | SYNTAX ERROR: data instructions must be of the following format -> label : value")
            exit(1)
            
        label, value = [x.strip() for x in inst.line.split(':')]
        
        target_lookup[label] = str(start_index + i)
        
        ### TODO: Add Arrays
        
        if value.isdigit():
            value = hex(int(value))
            
        if value.startswith("0x"):
            if len(value) > 6:
                print(f"LINE {inst.line_num} | SYNTAX ERROR: number too big")
            elif len(value) < 6:
                value = "0" * (6 - len(value)) + value[2:]
            else:
                value = value[2:]
        else:
            print(f"LINE {inst.line_num} | SYNTAX ERROR: data instructions must be of the following format -> label : value")
            exit(1)
            
        data_lines.append(value)
        
    return data_lines, target_lookup


def parse_text_segment(instructions: list[Instruction], target_lookup: dict) -> list[str]:
    result = []
    
    for inst in instructions:
        if inst.line == 'quit':
            result.append('F000')
            break
        
        op, params_str = inst.line.split(" ", 1)  
        
        params = []  
        
        for arg in params_str.split(","):
            arg = arg.strip()
            if arg in target_lookup:
                arg = target_lookup[arg]
                
            if arg.isdigit():
                arg = hex(int(arg))
            if arg.startswith('0x'):
                arg = arg[2:].upper()
                
            params.append(arg)
            
        try:
            result.append(encode_instruction(op, params))
        except SyntaxError as e:
            print(f"LINE {inst.line_num} | {e}")
            exit(1)
            
    return result


def get_instructions(input_file: str):
    
    data_instructions: list[Instruction] = []
    text_instructions: list[Instruction] = []
    
    current_directive: Directive | None = None
    
    with open(input_file, "r") as f:
        for i, line in enumerate(f.readlines()):
            line_num: int = i+1
            line: str = line.split('//')[0].strip()
            
            # TODO: implement /**/ comments
            if line == "":
                continue
            
            if line == ".text":
                current_directive = Directive.text   
                continue 
            elif line == ".data":
                current_directive = Directive.data
                continue
                
            if current_directive == Directive.text:
                ### TODO: add line jumps
                text_instructions.append(Instruction(line, line_num))
            elif current_directive == Directive.data:
                data_instructions.append(Instruction(line, line_num))
                
    return data_instructions, text_instructions

def write_to_file(output_file: str, text_code: list[str], data_code: list[str]):
    
    def address_to_str(address: str):
        return "@" + "0" * (4 - len(hex(address)[2:])) + hex(address)[2:].upper()
    
    address = 0
    
    with open(output_file, "w") as f:
        print("// .text", file=f)
        
        for line in text_code:
            print(address_to_str(address), line, file=f)
            address += 1
        
        print("\n// .data", file=f)
        for line in data_code:
            print(address_to_str(address), line, file=f)
            address += 1
            
            
def main(args=sys.argv[1:]):
    
    if not args:
        print("ERROR: you must provide an input file and output file")
        exit(1)
    elif args[0] == "-h":
        print("USAGE: ./parser.py [input file] [output file]")
        exit(0)
    elif len(args) == 1:
        print("ERROR: you must provide an output file")   
        exit(1)    
        
    input_file = args[0]
    output_file = args[1]
    
    if not os.path.exists(input_file):
        print(f"ERROR: file {input_file} does not exist")
    
    
    data, text = get_instructions(input_file)
    
    data_code, target_lookup = parse_data_segment(data, len(text))
    
    text_code = parse_text_segment(text, target_lookup)
    
    write_to_file(output_file, text_code, data_code)
    
    
if __name__ == '__main__':
    main()