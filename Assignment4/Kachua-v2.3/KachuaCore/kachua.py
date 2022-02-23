#!/usr/bin/python3
Release="Kachua v2.3"

import ast
import sys
from kast.builder import astGenPass

sys.path.insert(0, '../Submission/')

import pickle
import time
import turtle
import argparse
from submission import *
from interpreter import *
from irgen import *
from fuzzer import *

def interpret(ir, params={}):
    # for stmt,pc in ir:
    #     print(str(stmt.__class__.__bases__[0].__name__),pc)
    inptr = ConcreteInterpreter(ir)
    terminated = False
    inptr.initProgramContext(params)
    while True:
        terminated = inptr.interpret()
        if terminated:
            break
    print("Program Ended.")


def cleanup():
    pass


def stopTurtle():
    turtle.bye()


if __name__ == '__main__':

    print(Release)
    print("------------")

    # process the command-line arguments
    cmdparser = argparse.ArgumentParser(
        description='Program Analysis Framework for Turtle.')

    # add arguments for parsing command-line arguments
    cmdparser.add_argument(
        '-p', '--ir', action='store_true', help='pretty printing')
    cmdparser.add_argument(
        '-r', '--run', action='store_true', help='execute program')
    cmdparser.add_argument('-O', '--opt', action='store_true', help='optimize')
    cmdparser.add_argument(
        '-b', '--bin', action='store_true', help='load binary IR')
    cmdparser.add_argument(
        '-z', '--fuzz', action='store_true', help="Run fuzzer on a turtle program (seed values with '-d' or '--params' flag needed.)")
    cmdparser.add_argument(
        '-t', '--timeout', default=10, type=float, help='Timeout Parameter for Analysis (in secs)')
    cmdparser.add_argument('progfl')

    # passing variable values via command line. E.g.
    # ./kachua.py -r <program file> --params '{":x" : 10, ":z" : 20, ":w" : 10, ":k" : 2}'
    cmdparser.add_argument('-d', '--params', default=dict(),  type=ast.literal_eval,
                           help="pass variable values to kachua program in python dictionary format")
    # TODO: add additional arguments for parsing command-line arguments

    args = cmdparser.parse_args()

    if not (type(args.params) is dict):
        raise ValueError(
            "Wrong type for command line arguement '-d' or '--params'.")

    # generate IR
    if args.bin: 
        ir = loadIR(args.progfl)
    else:
        parseTree = getParseTree(args.progfl)
        astgen = astGenPass()
        ir = astgen.visitStart(parseTree)

    if args.opt:
        ir2 = optimize(ir)
        ir = ir2
        dumpIR("optimized.kw", ir)
        
    if args.ir:
        pretty_print(ir)

    if True:
        cfg = genCFG(ir)
        dumpCFG(cfg)

    if args.fuzz:
        if not args.params:
            raise RuntimeError("Fuzzing needs initial seed values. Specify using '-d' or '--params' flag.")
        """
        How to run fuzzer?
        # ./kachua.py -t 100 --fuzz example/fuzz2.tl -d '{":x": 5, ":y": 100}'
        # ./kachua.py -t 100 --fuzz example/example2.tl -d '{":dir": 3, ":move": 5}'
        """
        cov, corpus = fuzzMain(ir, args.params, timeLimit=args.timeout)
        print(f"Coverage : {cov},\nCorpus:")
        for index, x in enumerate(corpus):
            print(f"Input {index} : {x.data}")

    if args.run:
        interpret(ir, args.params)
        print()
        print("Press ESCAPE to exit")
        turtle.listen()
        turtle.onkeypress(stopTurtle, "Escape")
        turtle.mainloop()
