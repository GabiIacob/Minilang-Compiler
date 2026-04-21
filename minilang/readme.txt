Lexer
Lexer-ul transforma codul sursa in token-uri, adica elemente simple precum identificatori, numere, operatori si cuvinte cheie. El elimina spatiile si comentariile si pregateste codul pentru analiza sintactica.

named groups
('INT', r'\d+') → (?P<INT>\d+)

Parser
Parserul ia token-urile si le transforma intr-un AST (Abstract Syntax Tree). Aici se stabileste structura programului si ordinea operatiilor, iar instructiunile devin noduri conectate logic.

Semantic Analyzer
Analizorul semantic verifica daca programul are sens. El nu se uita la structura, ci la „semnificatie”: daca variabilele exista, daca tipurile sunt compatibile si daca operatiile sunt valide (ex: nu aduni string cu numar).

AST Nodes
Acestea sunt clasele care definesc limbajul intern al compilatorului (IntNode, BinOpNode, IfNode etc.). Ele nu executa nimic, ci doar reprezinta structura programului intr-o forma usor de procesat.

IR Generator
IR Generatorul transforma AST-ul intr-un cod intermediar (IR), adica instructiuni simple de tip 3-address code. Aici expresiile complexe sunt sparte in pasi simpli si se introduc variabile temporare si jump-uri.

Optimizer
Optimizerul imbunatateste IR-ul prin eliminarea codului inutil si simplificarea expresiilor (constant folding, dead code elimination). Scopul lui este sa reduca munca inainte de generarea codului final.

Code Generator
Code Generatorul transforma IR-ul in cod assembly (NASM x86_64). El traduce operatiile abstracte in instructiuni reale de procesor, lucrand cu registre si memorie.

Linker
Linkerul ia fisierul assembly, il asambleaza in obiect (.o) cu NASM si apoi il leaga cu GCC impreuna cu librariile sistemului pentru a produce executabilul final (.exe sau binar).

registre utilizate:

RAX – rezultat
RDI – primul parametru functie
RSI – al doilea parametru
LEA – ia adresa
XOR EAX,EAX – pune 0
SETE AL – 1 daca egal
MOVZX – extinde valoare
IDIV – impartire
RDX – restul impartirii

reguli parser:

parse_expr
→ parse_or
→ parse_and
→ parse_equality
→ parse_comparison
→ parse_term
→ parse_factor
→ parse_unary
→ parse_primary

flux compilare:

Source Code
Lexer (token-uri)
Parser (AST)
Semantic Analyzer (verificare sens)
AST Nodes (structura interna)
IR Generator (cod intermediar)
Optimizer (cod optimizat)
Code Generator (assembly)
NASM (object file .o)
Linker (GCC + libc)
Executable (.exe / bin)


LEXER
  ('ID', 'x')
  ('OP', '=')
  ('INT', '10')
  ('SEMICOLON', ';')
  ('ID', 'y')
  ('OP', '=')
  ('ID', 'x')
  ('OP', '*')
  ('INT', '2')
  ('OP', '+')
  ('INT', '5')
  ('SEMICOLON', ';')
  ('ID', 'if')
  ('LPAREN', '(')
  ('ID', 'y')
  ('OP', '>')
  ('INT', '20')
  ('RPAREN', ')')
  ('LBRACE', '{')
  ('ID', 'print')
  ('LPAREN', '(')
  ('ID', 'y')
  ('RPAREN', ')')
  ('SEMICOLON', ';')
  ('RBRACE', '}')

PARSER
  AssignNode(name='x', value=IntNode(value=10))
  AssignNode(name='y', value=BinOpNode(left=BinOpNode(left=VarNode(name='x'), op='*', right=IntNode(value=2)), op='+', right=IntNode(value=5)))
  IfNode(condition=BinOpNode(left=VarNode(name='y'), op='>', right=IntNode(value=20)), body=[PrintNode(expression=VarNode(name='y'))], else_body=None)

SEMANTIC
  Tabela simboluri: {'x': 'int', 'y': 'int'}

IR
  x = 10
  t1 = x * 2
  t2 = t1 + 5
  y = t2
  t3 = y > 20
  IF_FALSE t3 GOTO L1
  PRINT y
  L1:

OPTIMIZER
  x = 10
  t1 = x * 2
  t2 = t1 + 5
  y = t2
  t3 = y > 20
  IF_FALSE t3 GOTO L1
  PRINT y
  L1:

CODEGEN
global main
extern printf

section .text
main:
    push rbp
    mov rbp, rsp

    mov rax, 10
    mov [x], rax
    mov rax, [x]
    mov rcx, 2
    imul rax, rcx
    mov [t1], rax
    mov rax, [t1]
    mov rcx, 5
    add rax, rcx
    mov [t2], rax
    mov rax, [t2]
    mov [y], rax
    mov rax, [y]
    mov rcx, 20
    cmp rax, rcx
    setg al
    movzx rax, al
    mov [t3], rax
    mov rax, [t3]
    cmp rax, 0
    je L1
    sub rsp, 32
    mov rdx, [y]
    lea rcx, [fmt]
    xor eax, eax
    call printf
    add rsp, 32
L1:
    mov eax, 0
    pop rbp
    ret

section .data
fmt db "%d", 10, 0

section .bss
t2 resq 1
t1 resq 1
t3 resq 1
y resq 1
x resq 1
