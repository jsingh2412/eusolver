from eusolver import DCSolve
import ctypes

# Load the SynthLib2Parser shared library
synthlib2parser = ctypes.CDLL('../../synthlib2parser/lib/debug/libsynthlib2parser.so')

# Define the function prototypes
synthlib2parser.SynthLib2Parser_new.restype = ctypes.c_void_p
synthlib2parser.SynthLib2Parser_delete.argtypes = [ctypes.c_void_p]
synthlib2parser.SynthLib2Parser_parse.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
synthlib2parser.SynthLib2Parser_get_program.restype = ctypes.c_char_p
synthlib2parser.SynthLib2Parser_get_program.argtypes = [ctypes.c_void_p]

def parse_sygus_benchmark(file_path):
    # Create a new parser instance
    parser = synthlib2parser.SynthLib2Parser_new()

    # Parse the file
    synthlib2parser.SynthLib2Parser_parse(parser, file_path.encode('utf-8'))

    # Get the parsed program
    program = synthlib2parser.SynthLib2Parser_get_program(parser)

    # Delete the parser instance
    synthlib2parser.SynthLib2Parser_delete(parser)

    return program

def load_benchmark(file_path):
    return parse_sygus_benchmark(file_path)

def benchmark_test():
    benchmark_file = './benchmarks/initials.sl'

    components = load_benchmark(benchmark_file)
    print(components)
    solver = DCSolve(components.term_grammar, components.predicate_grammar, components.spec)

    result = solver.solve()
    print("Result of the benchmark test:", result)

if __name__ == "__main__":
    benchmark_test()