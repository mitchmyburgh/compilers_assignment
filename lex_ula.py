#----------------------------------------------
# lex_ula.py
#
# Lexical Analyser for the ula (unconventional language)
# By Mitch Myburgh (MYBMIT001)
# 12 09 2015
#----------------------------------------------

#import ply.lex
import ply.lex as lex
import fileinput # file input from terminal argument

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
    'COMMENT',
    'WHITESPACE'
)
##Literals - symbols used in ula
literals = ['#','&','@','$', '=', '(', ')' ]
# Regular expression rules for simple tokens
t_ID            = r'[a-zA-z_][a-zA-Z_0-9]*'
#Only ignore WHITESPACE and COMMENT if the file is imported
if __name__ == "__main__":
    t_WHITESPACE    = r'[\s]+' #\t\n\r
    t_COMMENT       = r'(\/\/.*)|\/\*+((([^\*])+)|([\*]+(?!\/)))[*]+\/'
else:
    t_ignore_WHITESPACE    = r'[\s]+' #\t\n\r
    t_ignore_COMMENT       = r'(\/\/.*)|\/\*+((([^\*])+)|([\*]+(?!\/)))[*]+\/'

##Regular expression for float literals
t_FLOAT_LITERAL = r'[\+-]?\d+(\d+)?(\.\d+)?([eE][\+-]?\d+)?'

##NOTE this affects the detecting of white space so is removed
# Define a rule so we can track line numbers
# def t_newline(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)

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
        if (tok.type in tokens_that_value_dont_get_printed): #print tokens that only the type get printed
            file.write(tok.type+"\n")
            print(tok.type)
        else: #print standard tokens
            file.write(tok.type+","+str(tok.value)+"\n")
            print(tok.type+","+str(tok.value))
    file.close()
