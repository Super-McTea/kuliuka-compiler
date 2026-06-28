from Lexer import Lexer
from Parser_RPN import Parser
from Compiler import Compiler
from AST import Program
import json
import time
import os

from argparse import ArgumentParser, Namespace

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float

def parse_arguments() -> Namespace:
    arg_parser: ArgumentParser = ArgumentParser(
        description="Kuliuka v0.0.1"
    )
    
    arg_parser.add_argument("file_path", type=str, help="Path to your entry point (i.e. main.klk)")
    arg_parser.add_argument("--debug", action="store_true", help="Prints internal debug info")
    
    return arg_parser.parse_args()

LEXER_DEBUG: bool = False
PARSER_DEBUG: bool = False
COMPILER_DEBUG: bool = False

RUN_CODE: bool = True

PROD_DEBUG: bool = False

if __name__ == '__main__':
    
    args = parse_arguments()
    
    if args.debug:
        PROD_DEBUG = True
    
    # Read from source file
    source_file = "main.klk"
    if args.file_path:
        source_file = args.file_path
        
    with open(source_file, "r") as f:
        code: str = f.read()
    
    if LEXER_DEBUG:
        print("===== LEXER DEBUG =====")
        debug_lex: Lexer = Lexer(source=code)
        while debug_lex.current_char is not None:
            print(debug_lex.next_token())
            
    l: Lexer = Lexer(source=code)
    p: Parser = Parser(lexer=l)
    
    parse_st: float = time.time()
    program: Program = p.parse_program()
    parse_et: float = time.time()
    
    if len(p.errors) > 0:
        for err in p.errors:
            print(err)
        exit(1)
    
    if PARSER_DEBUG:
        print("===== PARSER DEBUG =====")
        with open("debug/ast.json", 'w') as f:
            json.dump(program.json(), f, indent=4)
            
        print("Wrote AST to debug/AST.json successfully.")
        
    c: Compiler = Compiler(os.path.abspath(source_file))
    
    compiler_st: float = time.time()
    c.compile(node=program)
    compiler_et: float = time.time()
    
    # Output steps
    module: ir.Module = c.module
    module.triple = llvm.get_default_triple()
    
    if COMPILER_DEBUG:
        print("===== COMPILER DEBUG =====")
        with open("debug/ir.ll", "w") as f:
            f.write(str(module))
            
    if len(c.errors) > 0:
        print(f"==== COMPILER ERRORS ====")
        for err in c.errors:
            print(err)
        exit(1)
            
    if RUN_CODE:
        print("===== RUN CODE =====")
        
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        try:
            llvm_ir_parsed = llvm.parse_assembly(str(module))
            llvm_ir_parsed.verify()
        except Exception as e:
            print(e)
            raise
        
        target_machine = llvm.Target.from_default_triple().create_target_machine()
        
        module.data_layout = str(target_machine.target_data)
        
        engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
        engine.finalize_object()
        
        entry = engine.get_function_address('akamuri')
        cfunc = CFUNCTYPE(c_int)(entry)
        
        st = time.time()

        try:
            result = cfunc()
        except Exception as e:
            print(repr(e))
        
        et = time.time()
        
        if PROD_DEBUG:
            print(f"\n\n=== Parsed in: {round((parse_et - parse_st) * 1000, 6)} ms. ===")
            print(f"=== Compiled in: {round((compiler_et - compiler_st) * 1000, 6)} ms. ===")
        
        print(f"\n\nProgram returned: {result}\n=== Executed in {round((et - st) * 1000, 6)} ms. ===")
            