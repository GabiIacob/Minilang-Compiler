from parser.ast_nodes import (
    IntNode, FloatNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode,
    IfNode, WhileNode, PrintNode,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, kind=None, value=None):
        tok = self.peek()

        if tok is None:
            raise SyntaxError("Sfarsit neasteptat")


        if kind and tok[0] != kind:
            raise SyntaxError(f"Asteptat {kind}, primit {tok[0]}")


        if value and tok[1] != value:
            raise SyntaxError(f"Asteptat '{value}', primit '{tok[1]}'")

        self.pos += 1
        return tok

    def match(self, kind, value=None):
        tok = self.peek()
        return tok and tok[0] == kind and (value is None or tok[1] == value)

    
    def parse(self):
        stmts = []

        while self.peek() is not None:
            stmts.append(self.parse_statement())

        return stmts



    def parse_statement(self):
        if self.match('ID', 'if'):
            return self.parse_if()

        if self.match('ID', 'while'):
            return self.parse_while()

        if self.match('ID', 'print'):
            return self.parse_print()

        if self.match('ID'):
            return self.parse_assign()

        raise SyntaxError(f"Token neasteptat: {self.peek()}")

    def parse_assign(self):
        name = self.eat('ID')[1]
        self.eat('OP', '=')
        expr = self.parse_expr()
        self.eat('SEMICOLON')
        return AssignNode(name, expr)

    def parse_block(self):
        self.eat('LBRACE')
        body = []

        while not self.match('RBRACE'):
            body.append(self.parse_statement())

        self.eat('RBRACE')
        return body

    def parse_if(self):
        self.eat('ID', 'if')
        self.eat('LPAREN')
        cond = self.parse_expr()
        self.eat('RPAREN')

        body = self.parse_block()

        else_body = None
        if self.match('ID', 'else'):
            self.eat('ID', 'else')
            else_body = self.parse_block()

        return IfNode(cond, body, else_body)

    def parse_while(self):
        self.eat('ID', 'while')
        self.eat('LPAREN')
        cond = self.parse_expr()
        self.eat('RPAREN')

        body = self.parse_block()
        return WhileNode(cond, body)

    def parse_print(self):
        self.eat('ID', 'print')
        self.eat('LPAREN')
        expr = self.parse_expr()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return PrintNode(expr)

    
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()

        while self.match('OP', '||'):
            op = self.eat('OP')[1]
            right = self.parse_and()
            left = BinOpNode(left, op, right)

        return left

    def parse_and(self):
        left = self.parse_equality()

        while self.match('OP', '&&'):
            op = self.eat('OP')[1]
            right = self.parse_equality()
            left = BinOpNode(left, op, right)

        return left

    def parse_equality(self):
        left = self.parse_comparison()

        while self.match('OP') and self.peek()[1] in ('==', '!='):
            op = self.eat('OP')[1]
            right = self.parse_comparison()
            left = BinOpNode(left, op, right)

        return left

    def parse_comparison(self):
        left = self.parse_term()

        while self.match('OP') and self.peek()[1] in ('<', '>', '<=', '>='):
            op = self.eat('OP')[1]
            right = self.parse_term()
            left = BinOpNode(left, op, right)

        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.match('OP') and self.peek()[1] in ('+', '-'):
            op = self.eat('OP')[1]
            right = self.parse_factor()
            left = BinOpNode(left, op, right)

        return left

    def parse_factor(self):
        left = self.parse_unary()

        while self.match('OP') and self.peek()[1] in ('*', '/', '%'):
            op = self.eat('OP')[1]
            
            right = self.parse_unary()
            left = BinOpNode(left, op, right)

        return left

    def parse_unary(self):
        if self.match('OP', '!') or self.match('OP', '-'):
            op = self.eat('OP')[1]
            return UnaryOpNode(op, self.parse_unary())

        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()

        if tok is None:
            raise SyntaxError("Expresie incompleta")

        kind, val = tok

        if kind == 'INT':
            self.pos += 1
            return IntNode(int(val))

        if kind == 'FLOAT':
            self.pos += 1
            return FloatNode(float(val))

        if kind == 'BOOL':
            self.pos += 1
            return BoolNode(val == 'true')

        if kind == 'ID':
            self.pos += 1
            return VarNode(val)

        if kind == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expr()
            self.eat('RPAREN')
            return expr

        raise SyntaxError(f"Token neasteptat: {tok}")