#----------------------------------------------
# parse_ula.py
#
# Parser for the ula (unconventional language)
#----------------------------------------------
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lex_ula import tokens
import fileinput
# dictionary of names
names = { }

def p_program_stat(t):
    'program : statement'
    # print(t[1])
def p_program_clos(t):
    'program : program statement'
def p_statement_assign(t):
    'statement : ID "=" expression'
    # names[t[1]] = t[3]

def p_expression_op(t):
    '''expression : expression "@" term
                  | expression "$" term
                  | expression "#" term
                  | expression "&" term'''
    # if t[2] == '@' : t[0] = t[1] + t[3]
    # elif t[2] == '$': t[0] = t[1] - t[3]
    # elif t[2] == '#': t[0] = t[1] * t[3]
    # elif t[2] == '&': t[0] = t[1] / t[3]

def p_term_op(t):
    '''term   : term "#" factor
              | term "&" factor
              | factor'''
    # if t[2] == '#': t[0] = t[1] * t[3]
    # elif t[2] == '&': t[0] = t[1] / t[3]
    # else: print(t[1])

def p_factor_op(t):
    '''factor : "(" expression ")"
              | FLOAT_LITERAL
              | ID'''
    # if t[1] == '(': t[0] = t[2]
    # else: t[0] = t[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!"+repr(p))

# Build the parser
parser = yacc.yacc()
# Test it out
data = "a = 45"
# Build the data from the file name
# for line in fileinput.input():
#     data+=line


# while True:
result = parser.parse(data)
print(result)
