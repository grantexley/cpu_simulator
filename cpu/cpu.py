#!/usr/bin/env python3

"""
TODO:

Parser:
- add line labels
- negative branching
- add asm instruction comments
- add arrays

CPU:
- incorperate asm instruction comments
- a lot more testing and test files
- debugging info for branching
- negative branching
- complete main

Project:
- readme

"""

from datapath import Datapath
from controller import Controller
import sys

def main(args=sys.argv[1:]):

    input_file = args[0]
    
    datapath = Datapath(input_file)
    controller = Controller()
    
    while True:
        
        #this will exit when controller.state is "EX_QUIT"
        op, zero, neg = datapath.execute(controller.state)
        
        print('debug', datapath.debug)
        print(op, zero, neg)
        
        if datapath.debug: #true if we just finished cpu cycle
            instruction = hex(datapath.inst)[2:].upper()
            instruction = "0" * (4 - len(instruction)) + instruction
            pc = hex(datapath.pc)[2:].upper()
            pc = "0" * (4 - len(pc)) + pc
            print(f'{pc}: {instruction} | {datapath.debug}')
            input()
        
        controller.update_state(op, zero, neg)
        input()

if __name__ == '__main__':
    main()
    
    
    
