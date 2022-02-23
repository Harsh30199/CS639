#!/usr/bin/python3

import sys

sys.path.insert(0, './parser')
sys.path.insert(0, './ast')

from tlangLexer import tlangLexer
from tlangParser import tlangParser

from builder import *
from parseError import *

from submission import *

import antlr4
import argparse
import turtle

def IRGenerator(progfl):
    input_stream = antlr4.FileStream(progfl)
    print(input_stream)
    try:
        lexer = tlangLexer(input_stream)
        stream = antlr4.CommonTokenStream(lexer)
        lexer._listeners = [SyntaxErrorListener()]
        parser = tlangParser(stream)
        parser._listeners = [SyntaxErrorListener()]
        tree = parser.start()
    except Exception as e :
        print('\033[91m\n====================')
        print(e.__str__() + '\033[0m\n')
        exit(1)

    # instantiate visitor
    astgen = astGenPass()
    irlist = astgen.visitStart(tree)
    return irlist

def pretty_print(ir):
    print('========== IR ==========\n')
    for idx, item in enumerate(ir):
        print(idx, item[0], ' [', item[1], ']')


# TODO: move to a different file
class Interpreter:

    ir = None
    pc = None

    def __init__(self, ir):
        self.ir = ir
        self.pc = 0

    def interpret(self):
        stmt, tgt = self.ir[self.pc]
        # TODO: handle statement
        self.pc += tgt
        return False # TODO: return termination status

def interpret(ir):
    inptr = Interpreter(ir)
    terminated = False
    while True:
        terminated = inptr.interpret()
        if terminated:
            break
    print("Program Ended.")


   
if __name__ == '__main__':

    # process the command-line arguments
    cmdparser = argparse.ArgumentParser(description='Program Analysis Framework for Turtle.')

    # add arguments for parsing command-line arguments
    cmdparser.add_argument('progfl')
    # TODO: add addiotional arguments for parsing command-line arguments
    # cmdparser.add_argument('--print', help='pretty printing')
    # cmdparser.add_argument('--run', help='execute program')

    args = cmdparser.parse_args()

    # generate IR
    ir = IRGenerator(sys.argv[1])

    if True: # TODO: --print IR cmd option
        pretty_print(ir)

    if True:
        cfg = genCFG(ir)
        dumpCFG(cfg)
        
        
    if False: # TODO: --run option provided on command-line
        interpret(ir)
