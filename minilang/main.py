from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.semantic import SemanticAnalyzer
from ir.ir import IRGenerator
from optimizer.optimizer import Optimizer
from codegen.codegen import CodeGenerator
from linker.linker import Linker


CODE = """
x = 10;
y = x * 2 + 5;
if (y > 20) {
    print(y);
}
"""


def show(title, items):
    print(f"\n{title}")
    for item in items:
        print(f"  {item}")


def main():
    tokens = Lexer(CODE).tokenize()
    show("LEXER", tokens)

    ast = Parser(tokens).parse()
    show("PARSER", ast)

    symbols = SemanticAnalyzer().analyze(ast)
    show("SEMANTIC", [f"Tabela simboluri: {symbols}"])

    ir = IRGenerator().generate(ast)
    show("IR", ir)

    ir = Optimizer(ir).optimize()
    show("OPTIMIZER", ir)

    asm = CodeGenerator(ir).generate()
    print(f"\nCODEGEN\n{asm}")

    with open("output.asm", "w") as f:
        f.write(asm)

    print("\nLINKER")
    Linker("output.asm").build()


if __name__ == "__main__":
    main()
