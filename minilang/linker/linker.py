import subprocess
import sys


class Linker:

    def __init__(self, asm_file="output.asm"):
        self.asm_file = asm_file
        self.obj_file = asm_file.replace(".asm", ".o")

        self.is_windows = sys.platform == "win32"
        self.exe_file = asm_file.replace(".asm", ".exe" if self.is_windows else "")

    def _run(self, cmd):
        print(" ".join(cmd))
        return subprocess.run(cmd).returncode == 0

    def build(self):
        fmt = "win64" if self.is_windows else "elf64"

        if not self._run(["nasm", "-f", fmt, self.asm_file, "-o", self.obj_file]):
            return False

        if not self._run(["gcc", self.obj_file, "-o", self.exe_file, "-no-pie"]):
            return False

        print("BUILD OK:", self.exe_file)
        return True