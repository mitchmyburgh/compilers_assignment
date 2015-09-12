#----------------------------------------------
# lex_ula.py
#
# Lexical Analyser for the ula (unconventional language)
#----------------------------------------------

#import
import ply.lex as lex
import fileinput
##Just print the value here
tokens_that_dont_get_printed = [
    'PLUS', #@
    'MINUS', #$
    'TIMES', ##
    'DIVIDE', #&
    'EQUALS', #=
    'LEFT_PAREN', #(
    'RIGHT_PAREN' #)
]
##Just print the type here
tokens_that_value_dont_get_printed = [
    'COMMENT',
    'WHITESPACE',
    '@','$','#','&', '=', '(', ')'
]
#List of token names
tokens = (
    'ID',
    'FLOAT_LITERAL',
    # 'PLUS', #@
    # 'MINUS', #$
    # 'TIMES', ##
    # 'DIVIDE', #&
    # 'EQUALS', #=
    # 'LEFT_PAREN', #(
    # 'RIGHT_PAREN', #)
    'COMMENT',
    'WHITESPACE'
)
literals = ['@','$','#','&', '=', '(', ')' ]
# Regular expression rules for simple tokens
t_ID            = r'[a-zA-z_][a-zA-Z_0-9]*'
# t_PLUS          = r'\@'
# t_MINUS         = r'\$'
# t_TIMES         = r'[#]'
# t_DIVIDE        = r'\&'
# t_EQUALS        = r'\='
# t_LEFT_PAREN    = r'\('
# t_RIGHT_PAREN   = r'\)'
if __name__ == "__main__":
    t_WHITESPACE    = r'[\s]+' #\t\n\r
    t_COMMENT       = r'(\/\/.*)|\/\*+((([^\*])+)|([\*]+(?!\/)))[*]+\/'#r'(\/\/.*)|(\/\*.*?\*\/)'
else:
    t_ignore_WHITESPACE    = r'[\s]+' #\t\n\r
    t_ignore_COMMENT       = r'(\/\/.*)|\/\*+((([^\*])+)|([\*]+(?!\/)))[*]+\/'#r'(\/\/.*)|(\/\*.*?\*\/)'
t_FLOAT_LITERAL = r'[\+-]?\d+(\d+)?([eE][\+-]?\d+)?'
# A regular expression rule with action code for FLOAT_LITERAL
#def t_FLOAT_LITERAL(t):
    #r'[\+-]?\d+(.\d+)?([eE][\+-]?\d+)?'
    #t.value = float(t.value)
    #return t

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
data = ""
# Build the data from the file name
for line in fileinput.input():
    data+=line

# Give the lexer some input
lexer.input(data)

# Tokenize
if __name__ == "__main__":
    file = open(fileinput.filename()[:-4]+".tkn", "w") #write to token file
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        if (tok.type in tokens_that_value_dont_get_printed):
            file.write(tok.type+"\n")
            print(tok.type)
        elif (tok.type in tokens_that_dont_get_printed):
            file.write(str(tok.value)+"\n")
            print(str(tok.value))
        else:
            file.write(tok.type+","+str(tok.value)+"\n")
            print(tok.type+","+str(tok.value))
    file.close()
