#----------------------------------------------
# errors_ula.py
#
# Error checker for the ula (unconventional language)
# By Mitch Myburgh (MYBMIT001)
# 24 09 2015
#----------------------------------------------

#import code from part 1
import lex_ula as lex
import parse_ula as parse

#import for handling files
import os
import sys

error_text = ["lexical error on line %s", "parse error on line %s", "semantic error on line %s"]

#get the lexical errors on each line
def get_lex_errors(infilename):
    infile = open(infilename, "r")
    line_no = [[],[]];
    # redefine error to get line numbers
    def t_error(t):
        line_no[0].append(t.lexer.lineno)
        line_no[1].append(t.lexpos)
        t.lexer.skip(1)
    # set lex.t_error to the new t_error
    lex.t_error = t_error
    #rebuild the lexer
    lexer = lex.lex.lex(module=lex)
    #lex the file
    lexer.input(infile.read())
    for token in lexer:
        pass

    return line_no

#get the parsing errors on each line
def get_parse_errors(infilename):
    line_no = [[],[]];
    def p_error(p):
        line_no[0].append(p.lexer.lineno)
        line_no[1].append(p.lexpos)
        pass
    parse.p_error = p_error
    parser = parse.yacc.yacc(module=parse)
    infile = open(infilename, "r")
    #print(infile.read())
    syntree = parser.parse(infile.read())
    return line_no
    parser = null

#gen the table for checking the syntax
sem_errs = []
def gen_table(tree,table =[], depth = 0):
    for item in tree[1]:
        if isinstance(item, tuple):
            if item[0] == "AssignStatement" and (not item[1][0].split(",")[1] in table):
                table.append(item[1][0].split(",")[1])
            elif item[0] == "AssignStatement":
                sem_errs.append(item[1][0].split(",")[2])
            elif item[0] == "IdentifierExpression" and (not item[1][0].split(",")[1] in table):
                sem_errs.append(item[1][0].split(",")[2])
            gen_table(item,table,depth + 1)



def get_semantic_errors(infilename):
    import parse_ula as parse

    infile = open(infilename, "r")
    #modify the functions to add a line number
    def p_factor_id(p):
        """factor : ID"""
        p[0] = ("IdentifierExpression", ["ID," + p[1]+","+str(p.lineno(1))])
    def p_statement(p):
        """Statement : ID '=' expression"""
        p[0] = ("AssignStatement", ["ID," + p[1]+","+str(p.lineno(1)), p[3]])
    parse.p_factor_id = p_factor_id
    parse.p_statement = p_statement
    ##reset the line numbers
    lexer = lex.lex.lex(module=lex)
    lexer.lineno = 1
    parser = parse.yacc.yacc(module=parse)
    syntree = parser.parse(infile.read())
    #check the semantics from the tree
    gen_table(syntree)
    return sem_errs

if len(sys.argv) == 2:
    infilename = sys.argv[1]
    if os.path.isfile(infilename):
        #infile = open(infilename, "r")
        #print out the errors
        outfilename = os.path.splitext(infilename)[0]+".err"
        outfile = open(outfilename, "w")
        lex_errs = get_lex_errors(infilename)
        if (not len(lex_errs[0]) == 0):
            print(error_text[0] % min(lex_errs[0]))
            print(error_text[0] % min(lex_errs[0]), file=outfile)
        else:
            parse_errs = get_parse_errors(infilename)
            if (not len(parse_errs[0]) == 0):
                print(error_text[1] % min(parse_errs[0]))
                print(error_text[1] % min(parse_errs[0]), file=outfile)
            else:
                semantic_errs = get_semantic_errors(infilename)
                if (not len(semantic_errs) == 0):
                    print(error_text[2] % min(semantic_errs[0]))
                    print(error_text[2] % min(semantic_errs[0]), file=outfile)
        outfile.close()
    else:
        print("Not a valid file")
else:
    print("Specify filename, e.g. lex_ula.ply my_program.ula")
