import re
import parser_cyk
import argparse
import os

class Token(object):
    def __init__(self, type, val, pos):
        self.type = type

    def __str__(self):
        return '%s' % (self.type)


class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    def __init__(self, rules, skip_whitespace=False):
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('[\S^\n]')

    def input(self, buf):
        self.buf = buf
        self.pos = 0

    def token(self):

        if self.pos >= len(self.buf):
            return None
        else:
            if self.skip_whitespace:
                m = self.re_ws_skip.search(self.buf, self.pos)

                if m:
                    self.pos = m.start()
                else:
                    return None

            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = Token(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok


            raise LexerError(self.pos)

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok

def read_files_input (filename) :
    with open(filename, "r") as f :
        return f.read()

def write_files_output(name_out) :
    with open(name_out, "w") as f :
        f.write("%s" % output)

if __name__ == '__main__':
    
    rules = [
        # RESERVED WORDS
        (r'\n',               'NEWLINE'),
        ('\\n',               'NEWLINE'),
        (r'False',           'FALSE'),
        (r'None',            'NONE'),
        (r'True',            'TRUE'),
        (r'and',             'AND'),
        (r'as',              'AS'),
        (r'break',           'BREAK'),
        (r'class',           'CLASS'),
        (r'continue',        'CONTINUE'),
        (r'def',             'DEF'),
        (r'elif',            'ELIF'),
        (r'else',            'ELSE'),
        (r'for',             'FOR'),
        (r'from',            'FROM'),
        (r'if',              'IF'),
        (r'import',          'IMPORT'),
        (r'in',              'IN'),
        (r'$is',              'IS'),
        (r'not',             'NOT'),
        (r'or',              'OR'),
        (r'pass',            'PASS'),
        (r'raise',           'RAISE'),
        (r'return',          'RETURN'),
        (r'while',           'WHILE'),
        (r'with',            'WITH'),
        (r'is$',              'COMPARE'),
        (r'not',             'COMPARE'),
        ('\d+',             'NUMBER'),
        ('[a-zA-Z_]\w*',    'IDENTIFIER'),
        ('[?]',              'IDENTIFIER'),
        # KOMPARASI
        (r'==|!=|>=|<=|>|<|in|not in|is|is not',   'KOMPARASI'),
        #ASSIGN
        ('=', 'ASSIGN'),     
        (r'\/\/=|\*\*=|\+=|\-=|\*=|\/=|\%=', 'ASSIGN'),
        #ARITHMETIC
        (r'[+]|[-]|[*]|[/]|[%]|\/\/|\*\*', 'ARITHMETIC'),
        # ETCS
        ('[:]',                 'COLON'),
        ('[.]',                 'DOT'),
        (',',                   'COMMA'),
        # PARENTHESIS
        ('[(]',              'LP'),
        ('[)]',              'RP'),
        ('\[',              'LSB'),
        ('\]',              'RSB'),
        ('\{',              'LCB'),
        ('[#]',             'KOMENTAR'),
        ('\'\'\'',          'KOMENTAR_MULTILINE'),
        ('\'',             'QUOTE'),
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='File Name')
    args = parser.parse_args()

    lx = Lexer(rules, skip_whitespace=True)
    filename = args.filename

    ipt = read_files_input(filename)
    lx.input(ipt)

    output = ''
    try:
        for tok in lx.tokens():
            if tok == '':
                output = output
            else:
                output += str(tok) + ' '
    except LexerError as err:
        print('LexerError at position %s' % err.pos)

    if not os.path.exists("__pycache__"):
        os.makedirs("__pycache__")

    with open('__pycache__/outputfile', 'w') as outfile:
        outfile.write(output.replace("NEWLINE","\n"))

    cyk = parser_cyk.Parser("__pycache__/outputfile")
    cyk.analisa_syntax(filename)