#----------------------------------------------
# lex_ula.py
#
# Lexical Analyser for the ula (unconventional language)
#----------------------------------------------

#import
import ply.lex as lex
import fileinput
tokens_that_dont_get_printed = [
    'PLUS', #@
    'MINUS', #$
    'TIMES', ##
    'DIVIDE', #&
    'EQUALS', #=
    'LEFT_PAREN', #(
    'RIGHT_PAREN' #)
]
tokens_that_value_dont_get_printed = [
    'COMMENT',
    'WHITESPACE'
]
#List of token names
tokens = (
    'ID',
    'FLOAT_LITERAL',
    'PLUS', #@
    'MINUS', #$
    'TIMES', ##
    'DIVIDE', #&
    'EQUALS', #=
    'LEFT_PAREN', #(
    'RIGHT_PAREN', #)
    'COMMENT',
    'WHITESPACE'
)
# Regular expression rules for simple tokens
t_ID          = r'[a-zA-z_][a-zA-Z_0-9]*'
t_PLUS        = r'\@'
t_MINUS       = r'\$'
t_TIMES       = r'[#]'
t_DIVIDE      = r'\&'
t_EQUALS      = r'\='
t_LEFT_PAREN  = r'\('
t_RIGHT_PAREN = r'\)'
t_WHITESPACE  = r'[\s\t\n\r]'
t_COMMENT     = r'(\/\/.*)|\/\*+((([^\*])+)|([\*]+(?!\/)))[*]+\/'#r'(\/\/.*)|(\/\*.*?\*\/)'

# A regular expression rule with action code for FLOAT_LITERAL
def t_FLOAT_LITERAL(t):
    r'[\+-]?\d+(.\d+)?([eE][\+-]?\d+)?'
    #t.value = float(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
-15.64E-25
'''
for line in fileinput.input():
    print(fileinput)
    data+=line
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    if (tok.type in tokens_that_value_dont_get_printed):
        print(tok.type)
    elif (tok.type in tokens_that_dont_get_printed):
        print(str(tok.value))
    else:
        print(tok.type+","+str(tok.value))
