#----------------------------------------------
# ir_ula.py
#
# Intermediate representation for the ula (unconventional language)
# By Mitch Myburgh (MYBMIT001)
# 24 09 2015
#----------------------------------------------

from llvmlite import ir
from ctypes import CFUNCTYPE, c_float
import llvmlite.binding as llvm

# code for the parser
from ply import yacc
from lex_ula import tokens
import os
import sys


start = "Start"


def p_start(p):
    """Start : Program"""
    p[0] = p[1]


def p_program_statements(p):
    """Program : Statements"""
    p[0] = ["Program", p[1]]


def p_statements(p):
    """Statements : Statements Statement
                    | Statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """Statement : ID '=' expression"""
    p[0] = ["=", [p[1]], p[3]]


def p_expression_plus(p):
    """expression : expression '@' term"""
    p[0] = ["@", p[1], p[3]]


def p_expression_minus(p):
    """expression : expression '$' term"""
    p[0] = ["$", p[1], p[3]]


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


def p_term_multiply(p):
    """term : term '#' factor"""
    p[0] = ["#", p[1], p[3]]


def p_term_divide(p):
    """term : term '&' factor"""
    p[0] = ["&", p[1], p[3]]


def p_term_factor(p):
    """term : factor"""
    p[0] = p[1]


def p_factor_expression(p):
    """factor : '(' expression ')'"""
    p[0] = p[2]


def p_factor_float(p):
    """factor : FLOAT_LITERAL"""
    p[0] = [p[1]]


def p_factor_id(p):
    """factor : ID"""
    p[0] = [p[1]]


def p_error(p):
    pass


def print_tree(tupletree, depth=0):
    print("\t"*depth, tupletree[0])
    for item in tupletree[1]:
        if isinstance(item, tuple):
            print_tree(item, depth + 1)
        else:
            print("\t"*(depth+1), item)


parser = yacc.yacc()

#main function for the parser
def main():
    global infilename
    if len(sys.argv) == 2:
        infilename = sys.argv[1]
        if os.path.isfile(infilename):
            infile = open(infilename, "r")
            syntree = parser.parse(infile.read())
            # print_tree(syntree)
            return syntree
        else:
            print("Not a valid file")
    else:
        print("Specify filename, e.g. parse_ula.ply my_program.ula")

##llvmlite stuff
last_var = "" # keeps track of the last var assigned
var_dict = {}  # var names associated with memory location

def code_gen(tree): # traverse tree recursively to generate code
    global last_var
    if tree[0] == "Program":
        for t in tree[1]:
            code_gen(t)
    elif tree[0] == "=":
        last_var = tree[1][0]
        var_dict[last_var] = builder.alloca(ir.FloatType())
        builder.store(code_gen(tree[2]), var_dict[last_var])
    elif tree[0] == "@":
        return(builder.fadd(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "$":
        return(builder.fsub(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "#":
        return(builder.fmul(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "&":
        return(builder.fdiv(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] in var_dict.keys():
        return builder.load(var_dict[tree[0]])
    elif isinstance(float(tree[0]), float):
        return(ir.Constant(ir.FloatType(), float(tree[0])))
#main function for the ir generator
def run():
    global builder
    tree = main()
    flttyp = ir.FloatType() # create float type
    fnctyp = ir.FunctionType(flttyp, ()) # create function type to return a float
    module = ir.Module(name="ula") # create module named "ula"
    func = ir.Function(module, fnctyp, name="main") # create "main" function
    block = func.append_basic_block(name="entry") # create block "entry" label
    builder = ir.IRBuilder(block) # create irbuilder to generate code
    code_gen(tree) # call code_gen() to traverse tree & generate code
    builder.ret(builder.load(var_dict[last_var])) # specify return value
    return module


if __name__ == "__main__":
    module = run()
    outfilename = os.path.splitext(infilename)[0]+".ir"
    outfile = open(outfilename, "w")
    print(str(module).strip())
    print(str(module).strip(), file = outfile)
    outfile.close()
