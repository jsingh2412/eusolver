from eusolver import DCSolve
from parsers.parser import SygusV2Parser
from parsers.printer import SygusV2ASTPrinter
from parsers.processor import SygusV2Processor
import ply.yacc as yacc
from pprint import pprint
from parsers.ast import ASTVisitor

def load_benchmark(file_path):
    parser = SygusV2Parser()
    with open(file_path, 'r') as file:
        data = file.read()
    result = parser.parse(data)
    return result

def benchmark_test():
    benchmark_file = './benchmarks/s1.sl'

    program = load_benchmark(benchmark_file)
    program_str = SygusV2ASTPrinter.run(program, None)
    # print(program_str)
    # solver = DCSolve(components.term_grammar, components.predicate_grammar, components.spec)
    for attr in dir(program):
        print("obj.%s = %r" % (attr, getattr(program, attr)))
    # each none empty line is a command, representated by a class in the ast file
    print(program.commands)
    # result = solver.solve()
    # print("Result of the benchmark test:", result)

if __name__ == "__main__":
    benchmark_test()