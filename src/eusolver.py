from parsers.ast import ConstraintCommand, SynthFunCommand, IdentifierTerm, LiteralTerm, FunctionApplicationTerm
import itertools

class DCSolve:
    def __init__(self, term_grammar, predicate_grammar, spec):
        self.term_grammar = term_grammar
        self.predicate_grammar = predicate_grammar
        self.spec = spec
        self.points = set()
        self.terms = set()
        self.predicates = set()
        self.cover = {}
        self.operators = ['+', '-', '*', '=', '<', '!=', '<=', '>', '>=']
        self.basic_terms = []
        self.finding_first_term = True

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
            # 3: terms ← ∅; preds ← ∅; cover ← ∅; DT = ⊥
            self.terms.clear()
            self.predicates.clear()
            self.cover.clear()
            decision_tree = None
            # Term solver
            self.term_solver()
            # Unifier
            while decision_tree is None:
                self.terms.add(self.next_distinct_term(self.points, self.terms, self.cover))
                self.predicates.update(self.enumerate_predicates(self.points))
                decision_tree = self.learn_decision_tree(self.terms, self.predicates)
            # Verifier
            e = self.expr(decision_tree)
            cexpt = self.verify(e, self.spec)
            if cexpt is None:
                return e
            self.points.add(cexpt)

    def term_solver(self):
        while any(self.cover[t] != self.points for t in self.terms):
                self.terms.add(self.next_distinct_term(self.points, self.terms, self.cover))
        return

    def next_distinct_term(self, pts, terms, cover):
        def enumerate_terms(self):
            if self.finding_first_term:
                for term in self.term_grammar:
                    if isinstance(term, FunctionApplicationTerm) :
                        if term.function_identifier.symbol not in self.operators: 
                            self.operators.append(term.function_identifier.symbol)
                    else:
                        self.basic_terms.append(term)

            for t in self.basic_terms:
                terms.add(t)

            for t1, t2 in itertools.product(self.basic_terms, repeat=2):
                for op in self.operators:
                    terms.add(f"({op} {t1} {t2})")
        while True:
            t = enumerate_terms(self)
            cover[t] = {pt for pt in pts if self.satisfies(t, pt)}
            if all(cover[t] != cover[t_prime] for t_prime in terms):
                return t

    def satisfies(self, term, pt):
        # Implement the logic to check if term satisfies the point pt
        pass