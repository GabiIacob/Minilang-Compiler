from parser.ast_nodes import (
    IntNode, FloatNode, BoolNode, VarNode,
    BinOpNode, UnaryOpNode, AssignNode,
    IfNode, WhileNode, PrintNode,
)





class IRGenerator:

    def __init__(self):
        self.code = []
        self.temps = 0
        self.labels = 0

    def new_temp(self):
        self.temps += 1
        return f"t{self.temps}"

    def new_label(self):
        self.labels += 1
        return f"L{self.labels}"

    def emit(self, line):
        self.code.append(line)

    def generate(self, stmts):
        for s in stmts:
            self.visit(s)
        return self.code

    def visit(self, node):
        if isinstance(node, IntNode):
            return self.v_IntNode(node)
        elif isinstance(node, FloatNode):
            return self.v_FloatNode(node)
        elif isinstance(node, BoolNode):
            return self.v_BoolNode(node)
        elif isinstance(node, VarNode):

            return self.v_VarNode(node)
        elif isinstance(node, BinOpNode):
            return self.v_BinOpNode(node)
        elif isinstance(node, UnaryOpNode):
            return self.v_UnaryOpNode(node)
        elif isinstance(node, AssignNode):
            return self.v_AssignNode(node)
        elif isinstance(node, IfNode):  
            return self.v_IfNode(node)
        elif isinstance(node, WhileNode):
            return self.v_WhileNode(node)
        elif isinstance(node, PrintNode):
            return self.v_PrintNode(node)

    def v_IntNode(self, n):   
        return str(n.value)
    
    def v_FloatNode(self, n): 
        return str(n.value)
    
    def v_BoolNode(self, n):  
        return "1" if n.value else "0"
    
    def v_VarNode(self, n):   
        return n.name

    def v_AssignNode(self, n):
        val = self.visit(n.value)
        self.emit(f"{n.name} = {val}")

    def v_BinOpNode(self, n):
        l, r = self.visit(n.left), self.visit(n.right)
        t = self.new_temp()
        self.emit(f"{t} = {l} {n.op} {r}")
        return t

    def v_UnaryOpNode(self, n):
        v = self.visit(n.operand)

        t = self.new_temp()
        self.emit(f"{t} = {n.op}{v}")
        return t

    def v_IfNode(self, n):
        cond = self.visit(n.condition)
        end = self.new_label()
        if n.else_body:
            l_else = self.new_label()
            self.emit(f"IF_FALSE {cond} GOTO {l_else}")
            for s in n.body: 
                self.visit(s)
            self.emit(f"GOTO {end}")
            self.emit(f"{l_else}:")
            for s in n.else_body: 
                self.visit(s)
        else:

            self.emit(f"IF_FALSE {cond} GOTO {end}")
            for s in n.body: 
                self.visit(s)
        self.emit(f"{end}:")

    def v_WhileNode(self, n):
        start, end = self.new_label(), self.new_label()
        self.emit(f"{start}:")
        cond = self.visit(n.condition)
        self.emit(f"IF_FALSE {cond} GOTO {end}")
        for s in n.body: 
            self.visit(s)
        self.emit(f"GOTO {start}")
        self.emit(f"{end}:")

    def v_PrintNode(self, n):
        v = self.visit(n.expression)
        self.emit(f"PRINT {v}")
