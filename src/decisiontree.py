class Node:
    def __init__(self, predicate=None, term=None, left=None, right=None):
        self.predicate = predicate
        self.term = term
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.term is not None

class DecisionTree:
    def __init__(self):
        self.root = None

    def add_node(self, predicate, term_true, term_false):
        if self.root is None:
            self.root = Node(predicate, None, Node(None, term_true), Node(None, term_false))
        else:
            self._add_node_recursive(self.root, predicate, term_true, term_false)

    def _add_node_recursive(self, node, predicate, term_true, term_false):
        if node.is_leaf():
            return
        if node.left is None:
            node.left = Node(predicate, None, Node(None, term_true), Node(None, term_false))
        elif node.right is None:
            node.right = Node(predicate, None, Node(None, term_true), Node(None, term_false))
        else:
            self._add_node_recursive(node.left, predicate, term_true, term_false)
            self._add_node_recursive(node.right, predicate, term_true, term_false)

    def evaluate(self, x, y):
        return self._evaluate_recursive(self.root, x, y)

    def _evaluate_recursive(self, node, x, y):
        if node.is_leaf():
            eval_result = eval(node.term.replace('x', str(x)))
            return eval_result == y
        eval_result = eval(node.predicate.replace('x', str(x)))
        if eval_result:
            return self._evaluate_recursive(node.left, x, y)
        else:
            return self._evaluate_recursive(node.right, x, y)

def verify_decision_tree(dt, pts):
    for x, y in pts:
        result = dt.evaluate(x, y)
        if not result:
            return False, (x, y)
    return True, None

def eval_safe(expr, x, y):
    try:
        return eval(expr.replace('x', str(x)).replace('y', str(y)))
    except:
        return False

def choose_best_term(terms, pts):
    while True:
        for term in terms:
            term_str = str(term)
            correct = True
            for pt in pts:
                evaluated = eval(term_str.replace('x', str(pt[0])))
                if evaluated != pt[1]:
                    correct = False
                    break
            if correct:
                return term
        return None

def learn_decision_tree(terms, predicates, pts):
    dt = DecisionTree()
    for predicate in predicates:
        # Split points based on predicate
        left_pts = [pt for pt in pts if eval_safe(predicate, *pt)]
        right_pts = [pt for pt in pts if not eval_safe(predicate, *pt)]
        # Choose terms for left and right leaves
        left_term = choose_best_term(terms, left_pts)
        right_term = choose_best_term(terms, right_pts)
        if left_term is None or right_term is None:
            return None
        dt.add_node(predicate, left_term, right_term)

    return dt

def print_decision_tree(node, depth=0):
    if node is None:
        return
    indent = "  " * depth
    if node.is_leaf():
        print(f"{indent}Leaf: {node.term}")
    else:
        print(f"{indent}Predicate: {node.predicate}")
        print(f"{indent}Left:")
        print_decision_tree(node.left, depth + 1)
        print(f"{indent}Right:")
        print_decision_tree(node.right, depth + 1)

def decision_tree_to_ite_expression(node):
    if node.is_leaf():
        return node.term
    left_expr = decision_tree_to_ite_expression(node.left)
    right_expr = decision_tree_to_ite_expression(node.right)
    return f"if ({node.predicate}) then ({left_expr}) else ({right_expr})"

# pts = [(0, 0), (1, 10), (2, 20), (3, 30), (4, 40), (5, 5), (6, 6), (7, 7), (10, 10)]
# terms = ['x', 10, 20, 30, 40, 50]
# predicates = ['x <= (10 - x)']
# dt = learn_decision_tree(terms, predicates, pts)
# if dt is not None: print_decision_tree(dt.root)
# spec = 'result == 0 if x == y else (result == 1 if x > y else result == -1)'
# is_valid, counterexample = verify_decision_tree(dt, pts, spec)
# print("Is the decision tree valid?", is_valid)
# print("Counterexample:", counterexample)