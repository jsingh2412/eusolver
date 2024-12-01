from eusolver import DCSolve
import os

def load_benchmark(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def benchmark_test():
    # Define the path to the benchmark file
    benchmark_file = os.path.join('src', 'benchmarks', 'firstname.sl')

    # Load the benchmark constraints
    

    # Initialize the DCSolve instance
    solver = DCSolve(term_grammer, predicate_grammar, spec)

    # Run the solver
    result = solver.solve()

    # Print the result
    print("Result of the benchmark test:", result)

if __name__ == "__main__":
    benchmark_test()