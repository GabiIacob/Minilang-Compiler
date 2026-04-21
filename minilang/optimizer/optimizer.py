import re


class Optimizer:
    def __init__(self, ir):
        self.ir = list(ir)


    def optimize(self):
        self.ir = [self.fold(instr) for instr in self.ir]
        
        self.ir = self.remove_dead_code(self.ir)
        return self.ir


    def fold(self, instr):
        parts = instr.split()

        if len(parts) == 5 and parts[1] == '=':
            dest, a, op, b = parts[0], parts[2], parts[3], parts[4]

           
            if a.isdigit() and b.isdigit():
                a, b = int(a), int(b)

                if op == '+':

                    return f"{dest} = {a + b}"
                if op == '-':
                    return f"{dest} = {a - b}"
                if op == '*':
                    return f"{dest} = {a * b}"
                if op == '/' and b != 0:
                    return f"{dest} = {a // b}"

            
            if op == '+' and b == '0':
                return f"{dest} = {a}"
            if op == '+' and a == '0':
                return f"{dest} = {b}"

            if op == '-' and b == '0':
                return f"{dest} = {a}"

            if op == '*':

                if a == '1':
                    return f"{dest} = {b}"
                if b == '1':
                    return f"{dest} = {a}"

            if op == '*':
                if a == '0' or b == '0':
                    return f"{dest} = 0"

        if len(parts) == 5 and parts[1] == '=':
            dest, a, op, b = parts[0], parts[2], parts[3], parts[4]

            if a.isdigit() and b.isdigit():
                a, b = int(a), int(b)




                ops = {
                    '==': a == b,
                    '!=': a != b,
                    '<': a < b,
                    '>': a > b
                }

                if op in ops:
                    return f"{dest} = {int(ops[op])}"

        return instr

    def remove_dead_code(self, instrs):
        used = set()

        for instr in instrs:
            if instr.startswith("PRINT"):
                used.add(instr.split()[1])

            if "IF_FALSE" in instr:
                used.add(instr.split()[1])

            parts = instr.replace("=", " = ").split()
            for p in parts:
                if p.startswith("t"):
                    used.add(p)

        result = []

        for instr in instrs:
            if "=" in instr and not instr.endswith(":"):
                dest = instr.split("=")[0].strip()

                if dest.startswith("t") and dest not in used:
                    continue

            result.append(instr)

        return result