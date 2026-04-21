# 🧠 Simple Compiler

A simplified compiler that goes through all the classic stages: from source code to executable.

---

## 📌 Compilation Stages

### 1. Lexer

Transforms source code into **tokens** (identifiers, numbers, operators, etc.).

* Removes whitespace and comments
* Prepares input for the parser

**Example:**

```python
('INT', r'\d+') → (?P<INT>\d+)
```

---

### 2. Parser

Transforms tokens into an **AST (Abstract Syntax Tree)**.

* Defines program structure
* Handles operator precedence

---

### 3. Semantic Analyzer

Checks if the program is **semantically correct**:

* Variables are defined
* Types are compatible
* Operations are valid

---

### 4. AST Nodes

Internal representation of the program:

* `IntNode`
* `BinOpNode`
* `IfNode`

These **do not execute code**, they only describe it.

---

### 5. IR Generator

Transforms AST into **Intermediate Representation (3-address code)**:

* Breaks complex expressions
* Introduces temporary variables
* Adds jumps and labels

---

### 6. Optimizer

Improves the intermediate code:

* Constant folding
* Dead code elimination

---

### 7. Code Generator

Generates **Assembly code (NASM x86_64)**.

---

### 8. Linker

* NASM → `.o` object file
* GCC → final executable

---

## 🔄 Compilation Flow

```
Source Code
   ↓
Lexer
   ↓
Parser
   ↓
Semantic Analyzer
   ↓
IR Generator
   ↓
Optimizer
   ↓
Code Generator
   ↓
NASM (.o)
   ↓
Linker (GCC)
   ↓
Executable
```

---

## ⚙️ Registers Used

* `RAX` – result
* `RDI` – first function argument
* `RSI` – second argument
* `RDX` – remainder (division)
* `RCX` – auxiliary register

### Important Instructions:

* `LEA` – load address
* `XOR EAX, EAX` – set to 0
* `SETE AL` – set to 1 if equal
* `MOVZX` – zero-extend value
* `IDIV` – division

---

## 🧩 Parser Rules (Precedence)

```
parse_expr
→ parse_or
→ parse_and
→ parse_equality
→ parse_comparison
→ parse_term
→ parse_factor
→ parse_unary
→ parse_primary
```

---

## 📥 Example

### Input

```c
x = 10;
y = x * 2 + 5;

if (y > 20) {
    print(y);
}
```

---

### Lexer Output

```
('ID', 'x')
('OP', '=')
('INT', '10')
('SEMICOLON', ';')
...
```

---

### AST

```python
AssignNode(name='x', value=IntNode(10))
AssignNode(name='y', value=BinOpNode(...))
IfNode(...)
```

---

### Semantic Analyzer

```python
{'x': 'int', 'y': 'int'}
```

---

### IR (Intermediate Code)

```
x = 10
t1 = x * 2
t2 = t1 + 5
y = t2
t3 = y > 20
IF_FALSE t3 GOTO L1
PRINT y
L1:
```

---

### Assembly (NASM)

```asm
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
t1 resq 1
t2 resq 1
t3 resq 1
x resq 1
y resq 1
```

---

## 🚀 How to Run

```bash
nasm -f win64 program.asm -o program.o
gcc program.o -o program.exe
./program.exe
```
