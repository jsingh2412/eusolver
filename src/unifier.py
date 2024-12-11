import eusolver
from parsers.ast import FunctionApplicationTerm
class LIAUnifier:
    def __init__(self, predicate_grammar, points):
        self.predicate_grammar = predicate_grammar
        self.points = points
        self.first_run = True
        pass
    def reset(self):
        self.first_run = True
    def generate_preds(self, term_grammar, ret_one=False, max_depth=1, current_depth=1):
        if self.first_run:
            self.first_run = False
            terms = []
            operators = []
            for term in term_grammar:
                if isinstance(term, FunctionApplicationTerm):
                    if term.function_identifier.symbol not in operators:
                        if(term.function_identifier.symbol == 'ite'): pass
                        else: operators.append(term.function_identifier.symbol)
                else:
                    terms.append(term)

        if current_depth > max_depth:
            return []

        # generate more terms using operators
        new_terms = []
        for op in operators:
            for t1 in terms:
                for t2 in terms:
                    new_terms.append(f"({t1} {op} {t2})")
        terms.extend(new_terms)

        predicates = self.generate_relational_predicates(terms)
        #print('relational predicates:', predicates)
        if current_depth < max_depth:
            sub_predicates = self.generate_preds(term_grammar, max_depth, current_depth+1)
            #print("sub_predicates", sub_predicates)
            for p1 in sub_predicates:
                for p2 in sub_predicates:
                    predicates.append(f"({p1} and {p2})")
                    predicates.append(f"({p1} or {p2})")
                predicates.append(f"(not {p1})")
        valid_predicates = self.validate_predicates(predicates, self.points, ret_one)
        return valid_predicates

    def generate_relational_predicates(self, terms):
        predicates = []
        for t1 in terms:
            for t2 in terms:
                predicates.append(f"({t1} <= {t2})")
                predicates.append(f"({t1} >= {t2})")
                predicates.append(f"({t1} == {t2})")
        return predicates

    def validate_predicates(self, predicates, pts, ret_one=False):
        valid_predicates = []

        for predicate in predicates:
            is_useful = False
            true_set = set()
            false_set = set()

            for pt in pts:
                x = pt[0]
                substituted_predicate = predicate.replace("x", str(x))
                result = eval(substituted_predicate)
                if result:
                    true_set.add(x)
                else:
                    false_set.add(x)

            pts_len = len(pts)/2
            if len(true_set)>pts_len-1 and len(false_set)>pts_len-1:
                is_useful = True

            if is_useful:
                print('predicate:', predicate)
                print('true_set:', true_set)
                print('false_set:', false_set)
                if ret_one:
                    return predicate
                valid_predicates.append(predicate)

        return valid_predicates