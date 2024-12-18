from eusolver import DCSolve
from parsers.parser import SygusV2Parser
from parsers.printer import SygusV2ASTPrinter
from parsers.processor import SygusV2Processor
from parsers.ast import ConstraintCommand, SynthFunCommand, IdentifierTerm, LiteralTerm, FunctionApplicationTerm

# constraint that was temporarily removed from the .sl file: (constraint (or (and (> x 5) (= (f x) x)) (<= x 5)))

def load_benchmark(file_path):
    parser = SygusV2Parser()
    with open(file_path, 'r') as file:
        data = file.read()
    result = parser.parse(data)
    return result

def extract_args(program):
    synthfun = None
    spec = []
    for command in program.commands:
        if isinstance(command, SynthFunCommand):
            synthfun = command
        if isinstance(command, ConstraintCommand):
            spec.append(command)
    if synthfun is None:
        raise ValueError("[run_solver.extract_args] No synthesis function found in the benchmark file.")
    #pprint(synthfun.synthesis_grammar.grouped_rule_lists)
    # for rule in synthfun.synthesis_grammar.grouped_rule_lists:
    #     print(synthfun.synthesis_grammar)
    # synthfun_str = SygusV2ASTPrinter.run(synthfun, None)
    # print(synthfun_str)
    # for terminal in synthfun.synthesis_grammar.nonterminals:
    #     print(terminal)
    term_grammar = []
    start_symbol_found = False
    predicate_grammar = []
    startbool_symbol_found = False
    for grouped_rule_list in synthfun.synthesis_grammar.grouped_rule_lists.values():
        start_symbol_found = False
        startbool_symbol_found = False
        if(grouped_rule_list.head_symbol == "Start"):
            start_symbol_found = True
        elif(grouped_rule_list.head_symbol == "StartBool"):
            startbool_symbol_found = True
        else:
            raise ValueError("[run_solver.extract_args] Unknown head symbol.")
        for grammar in grouped_rule_list.expansion_rules:
            term = grammar.binder_free_term
            if isinstance(term, IdentifierTerm):
                #print(term.identifier)
                if start_symbol_found:
                    term_grammar.append(term.identifier.symbol)
                elif startbool_symbol_found:
                    predicate_grammar.append(term.identifier.symbol)
            if isinstance(term, LiteralTerm):
                #print(term.literal.literal_value, term.literal.literal_kind)
                if start_symbol_found:
                    term_grammar.append(term.literal.literal_value)
                elif startbool_symbol_found:
                    predicate_grammar.append(term.literal.literal_value)
            if isinstance(term, FunctionApplicationTerm):
                negative_number_found = False
                if(term.arguments.__len__() == 1 and isinstance(term.arguments[0], LiteralTerm)):
                    negative_number_found = True
                if start_symbol_found:
                    if(negative_number_found): term_grammar.append(0 - term.arguments[0].literal.literal_value)
                    else: term_grammar.append(term)
                elif startbool_symbol_found:
                    if(negative_number_found): term_grammar.append(0 - term.arguments[0].literal.literal_value)
                    else: predicate_grammar.append(term)
                #print(term.function_identifier)
                #for term in term.arguments: print(term.identifier)
    return term_grammar, predicate_grammar, spec

def benchmark_test():
    benchmark_file = './benchmarks/s2.sl'

    program = load_benchmark(benchmark_file)
    # program_str = SygusV2ASTPrinter.run(program, None)
    # print attributes of program object
    # for attr in dir(program):
    #     print("obj.%s = %r" % (attr, getattr(program, attr)))
    # each none empty line is a command, representated by a class in the ast file
    # print(program.commands)
    setlogic = program.commands[0]
    if(setlogic.logic_name == "LIA"):
        print("Logic is LIA")
    else:
        raise ValueError("[run_solver.benchmark_test] Solver is not capable of handling this logic.")

    term_grammar, predicate_grammar, spec = extract_args(program)

    print("Starting Solver:")
    print("Term Grammar:", term_grammar)
    print("Predicate Grammar:", predicate_grammar)
    print("Spec:", spec)
    solver = DCSolve(term_grammar, predicate_grammar, spec)
    result = solver.solve()
    print("Result of the benchmark test:", result)

if __name__ == "__main__":
    benchmark_test()