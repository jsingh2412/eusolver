from parsers.ast import LiteralTerm, FunctionApplicationTerm
import itertools
import eusolver

class TermSolver:
    def __init__(self, term_grammar, points, terms):
        self.points = points
        self.points_copy = points.copy()
        self.term_grammar = term_grammar
        self.cover = {}
        self.terms = terms
        # basis of operations provided by LIA
        self.operators = ['+', '-', '*'] #, '=', '<', '!=', '<=', '>', '>=']
        self.basic_terms = []
        self.finding_first_term = True
    def reset(self):
        self.points_copy = self.points.copy()
    def next_distinct_term(self, get_all=False):
        def enumerate_terms(self):
            if self.finding_first_term:
                self.finding_first_term = False
                for term in self.term_grammar:
                    if isinstance(term, FunctionApplicationTerm):
                        pass
                        #if term.function_identifier.symbol not in self.operators:
                            #self.operators.append(term.function_identifier.symbol)
                    else:
                        self.basic_terms.append(term)

            for t in self.basic_terms:
                if t not in self.terms:
                    covers, term, pts = self.evaluate_term(t)
                    if covers:
                        self.cover[term] = pts
                        if get_all:
                            print('covers:', covers, 'term:', term, 'pts:', pts)
                            return term
                        return term

            for t1, t2 in itertools.product(self.basic_terms, repeat=2):
                for op in self.operators:
                    if t not in self.terms:
                        term = (f"({t1} {op} {t2})")
                        covers, term, pts = self.evaluate_term(term)
                        if covers:
                            self.cover[term] = pts
                            if get_all:
                                print('covers:', covers, 'term:', term, 'pts:', pts)
                                return term
                            return term
        while True:
            t = enumerate_terms(self)
            if get_all and t not in self.terms: return t
            if t is None:
                return None
            print('cover:' , self.cover)
            if all(self.cover[t] != self.cover[t_prime] for t_prime in self.terms):
                self.cover[t] = {pt for pt in self.points if eusolver.satisfies(t, pt)}
                print("RETURNING T:",t)
                return t

    def evaluate_term(self, term):
        # if(type(term)== str and term.find('x') != -1):
        #     print(term)
        pts = []
        for pt in self.points_copy:
            str_term = str(term)
            if eval(str_term.replace('x', str(pt[0]))) == pt[1]:
                pts.append(pt)
            # if eusolver.satisfies(term, pt):
            #     #print("Something was satisfied:", term, pt)
            #     pts.append(pt)
        if len(pts) > 0:
            new_pts = [pt for pt in self.points_copy if pt not in pts]
            self.points_copy = new_pts
            return True, term, pts
        return False, None, None

    def solve(self):
        while True:
            self.terms.append(self.next_distinct_term())
            print('terms:', self.terms)
            print('cover', self.cover)
            print('points:', self.points)
            covered_points = set()
            for pts in self.cover.values():
                covered_points.update(pts)
            if covered_points == set(self.points):
                break
        return self.terms

    def generate_more_terms(self):
        while True:
            new_term = self.next_distinct_term()
            print('new_term:', new_term)
            if new_term is not None:
                self.terms.append(new_term)
            else: break