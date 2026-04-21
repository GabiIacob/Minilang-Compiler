import re


_VAR_RE = re.compile(r'^[A-Za-z_]\w*$')


class CodeGenerator:
    def __init__(self, ir):
        self.ir = ir
        self.asm = []
        self.vars = self._collect_vars()

    
    def _collect_vars(self):
        vars_set = set()

        for line in self.ir:
            if '=' in line:
                dest = line.split('=')[0].strip()
                if _VAR_RE.match(dest):
                    vars_set.add(dest)

        return vars_set

    
    def generate(self):
        self._header()

        for instr in self.ir:
            self._translate(instr)

        self._footer()
        return '\n'.join(self.asm)

   
    def _header(self):
        self.asm += [
            "default rel",
            "global main",
            "extern printf",
            "",
            "section .text",
            "main:",
            "    push rbp",
            "    mov rbp, rsp",
            "",
        ]

    def _footer(self):
        self.asm += [
            "    mov eax, 0",
            "    pop rbp",
            "    ret",
            "",
            "section .data",
            "fmt db \"%d\", 10, 0",
            "",
            "section .bss",
        ]

        for v in self.vars:
            self.asm.append(f"{v} resq 1")

  
    def _translate(self, instr):

        if instr.endswith(':'):
            self.asm.append(instr)
            return

        parts = instr.split()

        if parts[0] == 'GOTO':
            self.asm.append(f"    jmp {parts[1]}")
            return

        if parts[0] == 'IF_FALSE':
            self._if_false(parts)
            return

        if parts[0] == 'PRINT':
            self._print(parts)
            return

        if '=' in instr:
            self._assign(instr)

  
    def _if_false(self, parts):
        cond, label = parts[1], parts[3]

        self.asm += [
            f"    mov rax, [{cond}]",
            "    cmp rax, 0",
            f"    je {label}",
        ]

    def _print(self, parts):
        v = parts[1]

        self.asm += [
            "    sub rsp, 32",
            f"    mov rdx, [{v}]",
            "    lea rcx, [fmt]",
            "    xor eax, eax",
            "    call printf",
            "    add rsp, 32",
        ]

    def _assign(self, instr):
        dest, rhs = instr.split('=')
        dest = dest.strip()
        rhs = rhs.strip().split()

        if len(rhs) == 1:
            self._load('rax', rhs[0])
            self.asm.append(f"    mov [{dest}], rax")
            return

        if len(rhs) == 2:
            op, val = rhs
            self._load('rax', val)

            if op == '-':
                self.asm.append("    neg rax")
            elif op == '!':
                self.asm += [
                    "    cmp rax, 0",
                    "    sete al",
                    "    movzx rax, al",
                ]

            self.asm.append(f"    mov [{dest}], rax")
            return

        left, op, right = rhs

        self._load('rax', left)
        self._load('rcx', right)

        if op == '+':
            self.asm.append("    add rax, rcx")
        elif op == '-':
            self.asm.append("    sub rax, rcx")
        elif op == '*':
            self.asm.append("    imul rax, rcx")
        elif op == '/':
            self.asm += [
                "    cqo",
                "    idiv rcx",
            ]
        elif op == '%':
            self.asm += [
                "    cqo",
                "    idiv rcx",
                "    mov rax, rdx",
            ]

        elif op == '==':
            self.asm += ["    cmp rax, rcx", "    sete al", "    movzx rax, al"]
        elif op == '!=':
            self.asm += ["    cmp rax, rcx", "    setne al", "    movzx rax, al"]
        elif op == '<':
            self.asm += ["    cmp rax, rcx", "    setl al", "    movzx rax, al"]
        elif op == '>':
            self.asm += ["    cmp rax, rcx", "    setg al", "    movzx rax, al"]

        self.asm.append(f"    mov [{dest}], rax")

    
    def _load(self, reg, val):
        if val.lstrip('-').isdigit():
            self.asm.append(f"    mov {reg}, {val}")
        else:
            
            self.asm.append(f"    mov {reg}, [{val}]")