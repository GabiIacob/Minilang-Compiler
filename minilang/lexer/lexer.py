import re

KEYWORDS = {'if', 'else', 'while', 'print', 'true', 'false'}

TOKEN_SPEC = [
    ('COMMENT',   r'//.*'),                
    ('MCOMMENT',  r'/\*[\s\S]*?\*/'),      
    ('FLOAT',     r'\d+\.\d+'),
    ('INT',       r'\d+'),
    ('ID',        r'[A-Za-z_]\w*'),
    ('OP',        r'==|!=|<=|>=|&&|\|\||[+\-*/%<>=!]'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('LBRACE',    r'\{'),
    
    ('RBRACE',    r'\}'),
    ('SEMICOLON', r';'),
    ('SKIP',      r'[ \t\n\r]+'),
    ('MISMATCH',  r'.'),
]

parts = []

for name, pattern in TOKEN_SPEC:
    parts.append(f'(?P<{name}>{pattern})')

regex_pattern = '|'.join(parts)
_REGEX = re.compile(regex_pattern)

class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        for mo in _REGEX.finditer(self.code):
            kind, value = mo.lastgroup, mo.group()


            if kind in ('SKIP', 'COMMENT', 'MCOMMENT'):
                continue

            if kind == 'MISMATCH':
                raise RuntimeError(f"Caracter neasteptat: {value!r}")



            if kind == 'ID' and value in ('true', 'false'):
                kind = 'BOOL'

            tokens.append((kind, value))
        return tokens