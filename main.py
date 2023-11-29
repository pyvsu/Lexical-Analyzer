# CONSTANTS

DIGITS = '0123456789'
UALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LALPHA = UALPHA.lower()
KEYWORDS = ['balik','bool','des','desimal', 'doble', 'int','integro','ipakita', 'kar','karakter', 'kundi', 'kung', 'pangungusap', 'para', 'pasok', 'tigil', 'walangbalik']
RESWORDS = ['mali','magpatuloy','pumuntasa','simula', 'tama']
NOISEWORDS = ['imal', 'egro', 'akter']

# ERRORS

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
       super().__init__(pos_start, pos_end, 'Invalid', details)


# POSITION

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


# TOKENS

#arithmetic
inte = 'int'
flt = 'float'
add = 'addition'
sub = 'subtraction'
mul = 'multiplication'
div = 'division'
mod = 'modulo'
exp = 'exponent'

#relational
eq_to = 'equal to'
not_eq = 'not'
l_than = 'less than'
l_eq = 'less than/equal to'
g_than = 'greater than'
g_eq = 'greater than/equal to'

#logical
l_and = 'and'
l_or = 'or'

#assignment
assgn = 'assignment'
add_assgn = 'addition assignment'
sub_assgn = 'subtraction assignment'
mul_assgn = 'multiplication assignment'
div_assgn = 'division assignment'

#unary
inc = 'increment'
dec = 'decrement'

#comments
s_com = 'single line comment'
m1_com = 'multi line comment opening'
m2_com = 'multi line comment closing'

#delimeters
l_par = 'left parenthesis'
r_par = 'right parenthesis'
semicln = 'semicolon'
l_brack = 'left bracket'
r_brack = 'right bracket'
num_sign = "number sign"
open_q = "opening quote"


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


# LEXER


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.digit())
            elif self.current_char in UALPHA + LALPHA:
                tokens.append(self.str())
            elif self.current_char == '+':
                self.advance()
                if self.current_char == '+':
                    tokens.append(Token(inc))
                    self.advance()
                elif self.current_char == '=':
                    tokens.append(Token(add_assgn))
                    self.advance()
                else:
                    tokens.append(Token(add))
                    self.advance()
            elif self.current_char == '-':
                self.advance()
                if self.current_char == '-':
                    tokens.append(Token(dec))
                    self.advance()
                elif self.current_char == '=':
                    tokens.append(Token(sub_assgn))
                    self.advance()
                else:
                    tokens.append(Token(sub))
                    self.advance()
            elif self.current_char == '*':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(mul_assgn))
                    self.advance()
                else:
                    tokens.append(Token(mul))
                    self.advance()
            elif self.current_char == '/':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(div_assgn))
                    self.advance()
                elif self.current_char == '/':
                    tokens.append(Token(l_or))
                    self.advance()
                else:
                    tokens.append(Token(div))
                    self.advance()
            elif self.current_char == '(':
                tokens.append(Token(lpar))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(rpar))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(mod))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(exp))
                self.advance()
            elif self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(eq_to))
                    self.advance()
                else:
                    tokens.append(Token(assgn))
                    self.advance()
            elif self.current_char == '~':
                self.advance()
                if self.current_char == '^':
                    tokens.append(Token(m2_com))
                    self.advance()
                else:
                    tokens.append(Token(not_eq))
                    self.advance()
            elif self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(l_eq))
                    self.advance()
                else:
                    tokens.append(Token(l_than))
                    self.advance()
            elif self.current_char == '>':
                    self.advance()
                    if self.current_char == '=':
                        tokens.append(Token(g_eq))
                        self.advance()
                    else:
                        tokens.append(Token(g_than))
                        self.advance()
            elif self.current_char == '@':
                tokens.append(Token(l_and))
                self.advance()
            elif self.current_char == '^':
                self.advance()
                if self.current_char == '~':
                    tokens.append(Token(m1_com))
                    self.advance()
                else:
                    tokens.append(Token(s_com))
                    self.advance()
            elif self.current_char == ';':
                tokens.append(Token(semicln))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(l_brack))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(r_brack))
                self.advance()
            elif self.current_char == '#':
                tokens.append(Token(num_sign))
                self.advance()
            elif self.current_char == '"':
                tokens.append(Token(open_q))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def digit(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(inte, int(num_str))
        else:
            return Token(flt, float(num_str))

    def str(self):
        str = ''
        while self.current_char != None and (self.current_char in UALPHA or self.current_char in LALPHA):
            str += self.current_char
            self.advance()
        if str in KEYWORDS:
            return Token('keyword', str)
        elif str in RESWORDS:
            return Token('reserved words', str)
        else:
            return Token('identifier', str)


# RUN

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
