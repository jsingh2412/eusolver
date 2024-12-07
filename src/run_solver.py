from eusolver import DCSolve
from parsers.parser import SygusV2Parser
import ply.yacc as yacc

def load_benchmark(file_path):
    parser = SygusV2Parser()
    with open(file_path, 'r') as file:
        data = file.read()
    result = parser.parse(data)
    return result

def benchmark_test():
    benchmark_file = './benchmarks/s1.sl'

    components = load_benchmark(benchmark_file)
    print(components)
    # solver = DCSolve(components.term_grammar, components.predicate_grammar, components.spec)

    # result = solver.solve()
    # print("Result of the benchmark test:", result)

if __name__ == "__main__":
    benchmark_test()