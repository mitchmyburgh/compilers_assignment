#----------------------------------------------
# parse_ula.py
#
# Parser for the ula (unconventional language)
# By Mitch Myburgh (MYBMIT001)
# 12 09 2015
#----------------------------------------------
#import ply.yacc
import ply.yacc as yacc

# Get the token map from the lexer.
from lex_ula import tokens
import fileinput # file input from terminal argument

#Precendence
precedence = (
    ('left', '@', '$'),
    ('left', '#', '&'),
)

#Program is a statement
def p_program(p):
    '''program : statement'''
    p[0] = ('Start', ('Program', p[1]))

#Closure of the statement
def p_statement_clos(p):
    '''statement : statement statement'''
    p[0] = p[1]+ p[2]

#define a statement
def p_statement_assign(p):
    'statement : ID "=" expression'
    p[0] = ('AssignStatement', ("ID,"+ p[1],), p[3])

#Summation expression
def p_expression_sum(p):
    '''expression : expression "@" expression'''
    p[0] = ('AddExpression', p[1], p[3])

#Subtraction expression
def p_expression_sub(p):
    '''expression : expression "$" expression'''
    p[0] = ('SubExpression', p[1], p[3])

#expression goes to term
def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

#Term multiplication
def p_term_product(p):
    '''term : term "#" factor'''
    p[0] = ('MulExpression', p[1], p[3])


#Term Division
def p_term_div(p):
    '''term : term "&" factor'''
    p[0] = ('DivExpression', p[1], p[3])

#term goes to Factor
def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

#Factor goes to (Expression)
def p_factor_pare(p):
    '''factor : "(" expression ")"'''
    p[0] = p[2]

#Factor goes to FLOAT_LITERAL
def p_factor_float(p):
    '''factor : FLOAT_LITERAL'''
    p[0] = ("FloatExpression", ('FLOAT_LITERAL,'+p[1],))

#Factor goes to ID
def p_factor_ID(p):
    '''factor : ID'''
    p[0] = ('IdentifierExpression', ("ID,"+ p[1],))


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!"+repr(p))

# Build the parser
parser = yacc.yacc()
# Test it out
data = ""
# Build the data from the file name
for line in fileinput.input():
    data+=line


# while True:
result = parser.parse(data)
#Recursively generate the string representation of the tree
def genRec(res, n = -1):
    string = ""
    if isinstance(res, str):
        return "\t"*(n)+res+"\n"
    else:
        for i in res:
            string += genRec(i, n+1)
        return string

##Print the reult to the screen
print(genRec(result))
##print the result to the file
file = open(fileinput.filename()[:-4]+".ast", "w") #write to ast file
file.write(genRec(result))
file.close()
