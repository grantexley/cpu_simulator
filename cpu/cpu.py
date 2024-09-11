#!/usr/bin/env python3

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
        
        if datapath.debug: #true if we just finished cpu cycle
            instruction = hex(datapath.inst)[2:].upper()
            instruction = "0" * (4 - len(instruction)) + instruction
            pc = hex(datapath.pc)[2:].upper()
            pc = "0" * (4 - len(pc)) + pc
            print(f'{pc}: {instruction} | {datapath.debug}', end='')
            input()
        
        controller.update_state(op, zero, neg)

if __name__ == '__main__':
    main()
    
    
    
