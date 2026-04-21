from dataclasses import dataclass
from typing import Optional


@dataclass
class IntNode:
    value: int

@dataclass
class FloatNode:
    value: float

@dataclass
class BoolNode:
    value: bool

@dataclass
class VarNode:
    name: str

@dataclass
class BinOpNode:
    left: object
    op: str
    right: object

@dataclass
class UnaryOpNode:
    op: str
    operand: object

@dataclass
class AssignNode:
    name: str
    value: object

@dataclass
class IfNode:
    condition: object
    body: list
    else_body: Optional[list] = None

@dataclass
class WhileNode:
    condition: object
    body: list

@dataclass
class PrintNode:
    expression: object
