#!/usr/bin/env python3
from encoding import encode_instruction
import sys
import os


def parse_text_segment(lines: list[str], data: dict) -> str:
    result = []
    
    for line in lines:
        print(f'LINE: {line}')
    
        if line == 'quit':
            result.append('F000')
            break
        
        op, params_str = line.split(" ", 1)  
        
        params = []  
        
        for arg in params_str.split(","):
            arg = arg.strip()
            if arg in data:
                arg = data[arg]
                
            if arg.isdigit():
                arg = hex(int(arg))
                
            params.append(arg)
            
        encoded = encode_instruction(op, params)
        
        if encoded:
            result.append(encoded)
        else:
            print(f"SYNTAX ERROR: Could not parse '{line}'")
            exit(1)
    
    return "\n".join(result)


def parse_data_segment(lines: list[str]) -> dict:
    
    data = {}
    
    for line in lines:
        line = line.split('//')[0].strip()
        
        if ":" not in line:
            print("SYNTAX ERROR: data instructions must be of the following format -> label : value")
            
        label, value = line.split(':')
        
        data[label.strip()] = value.strip()
        
    return data


def parse_asm_file(input_file: str):
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f.readlines() ]
        
    # TODO: implement the ability to make arrays in data
    # TODO: implement /**/ comments
    
    result = ""
    line_number = 0
    data_index = -1
    text_index = -1

    #clean and find .text and .data directives
    while line_number < len(lines):
        line = lines[line_number]
        
        if line.startswith('//') or line == "":
            lines.pop(line_number)
            continue
        
        if line == '.data':
            data_index = line_number   
        if line == '.text': 
            text_index = line_number
            
        line_number += 1
            
    if text_index == -1:
        print("SYNTAX ERROR: could not find .text directive")
        exit(1)
    
    
    if data_index == -1: #no data segment
        data = {}
        text_segment = lines[text_index + 1:]
        
    else:
        
        if data_index < text_index: #data before text
            data = parse_data_segment(lines[data_index + 1 :text_index])
            text_segment = lines[text_index + 1 :]
        else: #text before data
            data = parse_data_segment(lines[data_index + 1 :])
            text_segment = lines[text_index + 1 :data_index]
            
    print("TEXT SEGMENT: ", text_segment)
    print("DATA: ", data)
    return parse_text_segment(text_segment, data)
      

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
    
    
    result = parse_asm_file(input_file)
    return
    with open(output_file, "w") as f:
        f.write(result)
    
if __name__ == '__main__':
    main()