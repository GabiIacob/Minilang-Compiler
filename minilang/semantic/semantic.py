from platform import node

from parser.ast_nodes import IntNode, FloatNode


ARITH = {'+', '-', '*', '/', '%'}
CMP   = {'==', '!=', '<', '>', '<=', '>='}
LOGIC = {'&&', '||'}


class SemanticAnalyzer:

    def __init__(self):
        self.symbols = {}

    def analyze(self, stmts):
        for s in stmts:
            self.visit(s)
        return self.symbols

    def visit(self, node):
        match type(node).__name__:
            case "IntNode":
                return self.v_IntNode(node)
            case "FloatNode":
                
                return self.v_FloatNode(node)
            case "BoolNode":
                return self.v_BoolNode(node)
            case "VarNode":
                return self.v_VarNode(node)
            case "AssignNode":
                return self.v_AssignNode(node)
            case "IfNode":
                return self.v_IfNode(node)
            case "WhileNode":
                return self.v_WhileNode(node)
            case "PrintNode":
                return self.v_PrintNode(node)
            case "BinOpNode":
                return self.v_BinOpNode(node)
            case "UnaryOpNode":
                return self.v_UnaryOpNode(node)
            case _:
                raise Exception(f"Nod necunoscut: {type(node).__name__}")

    def v_IntNode(self, n):   
        return 'int'
    def v_FloatNode(self, n): 
        return 'float'
    def v_BoolNode(self, n):  
        return 'bool'









    def v_VarNode(self, n):
        if n.name not in self.symbols:
            raise Exception(f"Variabila nedeclarata: {n.name}")
        return self.symbols[n.name]

    def v_AssignNode(self, n):
        t = self.visit(n.value)
        self.symbols[n.name] = t
        return t

    def v_IfNode(self, n):
        if self.visit(n.condition) != 'bool':

            raise Exception("Conditia 'if' trebuie sa fie bool")
        
        
        for s in n.body: 
            self.visit(s)   
        if n.else_body:
            for s in n.else_body: 
                self.visit(s)

    def v_WhileNode(self, n):
        if self.visit(n.condition) != 'bool':
            raise Exception("Conditia 'while' trebuie sa fie bool")
        for s in n.body: 
            self.visit(s)

    def v_PrintNode(self, n):
        return self.visit(n.expression)

    def v_BinOpNode(self, n):
        lt, rt = self.visit(n.left), self.visit(n.right)
        op = n.op
        if op in CMP:
            if lt != rt:
                raise Exception(f"Nu se pot compara {lt} si {rt}")
            return 'bool'
        if op in LOGIC:

            if lt != 'bool' or rt != 'bool':
                raise Exception(f"Operatorii logici cer bool")
            return 'bool'
        if op in ARITH:

            if 'bool' in (lt, rt):
                raise Exception("Aritmetica pe bool nu e permisa")
            if op in ('/', '%'):
                if isinstance(n.right, IntNode) and n.right.value == 0:
                    raise Exception("Impartire la zero")
                if isinstance(n.right, FloatNode) and n.right.value == 0.0:
                    raise Exception("Impartire la zero")
            return 'float' if 'float' in (lt, rt) else 'int'
        
        raise Exception(f"Operator necunoscut: {op}")

    def v_UnaryOpNode(self, n):
        t = self.visit(n.operand)
        if n.op == '!':
            if t != 'bool': raise Exception("! cere bool")
            return 'bool'
        if n.op == '-':
            if t == 'bool': raise Exception("Nu se poate nega un bool")
            return t
        raise Exception(f"Operator unar necunoscut: {n.op}")
