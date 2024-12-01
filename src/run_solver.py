from eusolver import DCSolve
import os
import re

def parse_sygus_benchmark(file_path):
    components = {
        "term_grammar": [],
        "predicate_grammar": [],
        "spec": []
    }

    with open(file_path, 'r') as file:
        lines = file.readlines()
    nt_string_section = False
    nt_bool_section = False
    for line in lines:
        line = line.strip()

        if "(ntString" in line:
            nt_string_section = True
        elif nt_string_section and re.match(r"\(nt(Int|Bool)", line):
            nt_string_section = False
        if nt_string_section and line.__len__() > 0:
            components["term_grammar"].append(line)
        if "(ntBool" in line:
            nt_bool_section = True
        elif nt_bool_section and line.startswith("(declare-var"):
            nt_bool_section = False
        if nt_bool_section and line.__len__() > 0:
            components["predicate_grammar"].append(line)
        elif line.startswith("(constraint"):
            constraint = line.replace("(constraint ", "").rstrip(")")
            components["spec"].append(constraint)

    return components


def load_benchmark(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def benchmark_test():
    benchmark_file = './benchmarks/initials.sl'

    components = parse_sygus_benchmark(benchmark_file)
    print(components)
    solver = DCSolve(components.term_grammr, components.predicate_grammar, components.spec)

    result = solver.solve()
    print("Result of the benchmark test:", result)

if __name__ == "__main__":
    benchmark_test()