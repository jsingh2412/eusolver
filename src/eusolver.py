from parsers.ast import LiteralTerm, FunctionApplicationTerm
from termsolver import TermSolver

class DCSolve:
    def __init__(self, term_grammar, predicate_grammar, spec):
        self.term_grammar = term_grammar
        self.predicate_grammar = predicate_grammar
        self.spec = spec
        self.points = []
        self.terms = []
        self.predicates = []
        self.cover = {}

    def solve(self):
        # Ensure: Expression e s.t. e ∈ [[G]] ∧ e |= Φ
        # 1: pts ← ∅
        # 2: while true do
        # 3: terms ← ∅; preds ← ∅; cover ← ∅; DT = ⊥
        # 4: while S t∈terms  cover[t] 6= pts do
        # 5: terms ← terms ∪ NextDistinctTerm(pts,terms, cover)
        # 6: while DT = ⊥ do . Unifier
        # 7: terms ← terms ∪ NextDistinctTerm(pts,terms, cover)
        # 8: preds ← preds ∪ enumerate(GP , pts)
        # 9: DT ← LearnDT(terms, preds)
        # 10: e ← expr(DT); cexpt ← verify(e, Φ) . Verifier
        # 11: if cexpt = ⊥ then return e
        # 12: pts ← pts ∪ cexpt
        # 13: function NextDistinctTerm(pts,terms, cover)
        # 14: while True do
        # 15: t ← enumerate(GT , pts); cover[t] ← {pt | pt ∈ pts ∧ t |= Φ  pt}
        # 16: if ∀t' ∈ terms : cover[t] != cover[t'] then return t
        while True:
            # self.terms.clear()
            # self.predicates.clear()
            # self.cover.clear()
            decision_tree = None
            self.generate_pts()
            print(self.points)
            # Term solver
            termsolver = TermSolver(self.term_grammar, self.points, self.cover, self.terms)
            self.terms = termsolver.solve()
            print(self.terms)
            # Unifier
            while decision_tree is None:
                self.terms.append(self.next_distinct_term())
                self.predicates.update(self.enumerate_predicates(self.points))
                decision_tree = self.learn_decision_tree(self.terms, self.predicates)
            # Verifier
            e = self.expr(decision_tree)
            cexpt = self.verify(e, self.spec)
            if cexpt is None:
                return e
            self.points.add(cexpt)

    def generate_pts(self):
        print('generate_pts')
        self.points = []
        for constraint in self.spec:
            if(constraint.constraint.function_identifier.symbol == "="):
                args = constraint.constraint.arguments
                if isinstance(args[0], FunctionApplicationTerm) and isinstance(args[1], LiteralTerm):
                    self.points.append((args[0].arguments[0].literal.literal_value, args[1].literal.literal_value))
                elif isinstance(args[1], FunctionApplicationTerm) and isinstance(args[0], LiteralTerm):
                    self.points.append((args[1].arguments[0].literal.literal_value, args[0].literal.literal_value))
        return

def satisfies(term, pt):
        if (type(term)== str and term.find('x') != -1):
            value = eval_sygus(term.replace("x", str(pt[0])), {'x': pt[0]})
            return value == pt[1]
        elif (type(term)== int):
            return term == pt[1]
        else:
            if(term != None):
                value = eval_sygus(term, {})
                return value == pt[1]
            return False

def eval_sygus(expr, variables):
        expr = expr.strip()
        # handle constants
        if expr.isdigit():
            return int(expr)
        # handle lone expression (for example, expr= 'x')
        if expr in variables:
            return variables[expr]
        # remove parantheses
        if expr.startswith("("):
            expr = expr[1:-1]
        tokens = expr.split(" ", 2)
        op = tokens[0]
        term1 = tokens[1]
        term2 = tokens[2] if len(tokens) > 2 else None

        # Recursive evaluation of terms
        value1 = eval_sygus(term1, variables) if term1 else None
        value2 = eval_sygus(term2, variables) if term2 else None

        # Apply operations
        if op == "+":
            return value1 + value2
        elif op == "-":
            return value1 - value2
        elif op == "*":
            return value1 * value2
        elif op == "/":
            return value1 // value2  # Integer division
        elif op == "<=":
            return value1 <= value2
        elif op == ">=":
            return value1 >= value2
        elif op == "=":
            return value1 == value2
        elif op == "and":
            return value1 and value2
        elif op == "or":
            return value1 or value2
        elif op == "not":
            return not value1
        # elif op == "ite":
        #     #if then else
        #     condition = value1
        #     true_expr = tokens[2].split(" ", 1)[0]
        #     false_expr = tokens[2].split(" ", 1)[1]
        #     return self.eval_sygus(true_expr, variables) if condition else self.eval_sygus(false_expr, variables)

        raise ValueError(f"Unsupported operation: {op}")