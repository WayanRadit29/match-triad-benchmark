import copy
from typing import Any, Callable, Dict, List, Tuple


def backtracking_csp(
    variables: List[Any],
    domains: Dict[Any, List[Any]],
    constraints: List[Tuple[Any, Any, Callable[[Any, Any], bool]]],
    soft_score: Callable[[Any, Any], float]
) -> Tuple[Dict[Any, Any], float]:
    """
    Generic CSP backtracking with MRV, forward‐checking, and soft‐constraint scoring.

    Args:
        variables: list of variable identifiers.
        domains: mapping var → list of possible values.
        constraints: list of binary constraints of form (X, Y, f)
                     where f(val_x, val_y) → True if consistent.
        soft_score: function(var, val) → float score for assigning val to var.

    Returns:
        best_assignment: mapping var → chosen val maximizing total soft score.
        best_score: the corresponding total soft score.
    """
    # Copy domains so original isn't mutated
    init_domains = {v: list(domains[v]) for v in variables}

    best_assignment: Dict[Any, Any] = {}
    best_score: float = float('-inf')

    def mrv(current_domains: Dict[Any, List[Any]], assignment: Dict[Any, Any]) -> Any:
        unassigned = [v for v in variables if v not in assignment]
        return min(unassigned, key=lambda v: len(current_domains[v]))

    def forward_check(
        var: Any,
        val: Any,
        current_domains: Dict[Any, List[Any]],
        assignment: Dict[Any, Any]
    ) -> Dict[Any, List[Any]]:
        """Prune neighbors' domains after assigning var=val."""
        new_domains = copy.deepcopy(current_domains)
        for (X, Y, cons) in constraints:
            # Prune domain of Y if constraint on (var, Y)
            if X == var and Y not in assignment:
                new_domains[Y] = [w for w in new_domains[Y] if cons(val, w)]
            # Prune domain of X if constraint on (X, var)
            if Y == var and X not in assignment:
                new_domains[X] = [w for w in new_domains[X] if cons(w, val)]
        return new_domains

    def recurse(
        assignment: Dict[Any, Any],
        current_domains: Dict[Any, List[Any]],
        curr_score: float
    ) -> None:
        nonlocal best_assignment, best_score

        # If fully assigned, update best
        if len(assignment) == len(variables):
            if curr_score > best_score:
                best_score = curr_score
                best_assignment = assignment.copy()
            return

        var = mrv(current_domains, assignment)
        for val in current_domains[var]:
            # Check hard constraints with already assigned vars
            valid = True
            for (X, Y, cons) in constraints:
                if X == var and Y in assignment and not cons(val, assignment[Y]):
                    valid = False; break
                if Y == var and X in assignment and not cons(assignment[X], val):
                    valid = False; break
            if not valid:
                continue

            # Tentative assign
            assignment[var] = val
            new_score = curr_score + soft_score(var, val)

            # Forward checking
            pruned_domains = forward_check(var, val, current_domains, assignment)
            # Continue only if no domain is empty
            if all(pruned_domains[v] for v in variables if v not in assignment):
                recurse(assignment, pruned_domains, new_score)

            # Undo assignment
            del assignment[var]

    # Start recursion
    recurse(assignment={}, current_domains=init_domains, curr_score=0.0)
    return best_assignment, best_score


# Contoh sederhana:

# Variabel
vars = ['A','B','C']

# Domain awal
doms = {
    'A': [1,2,3],
    'B': [1,2,3],
    'C': [1,2]
}

# Hard constraint: semua variabel harus berbeda
hard_cons = [
    ('A','B', lambda x,y: x!=y),
    ('A','C', lambda x,y: x!=y),
    ('B','C', lambda x,y: x!=y),
]

# Soft score: nilai var=val seberapa suka
soft = lambda var,val: {('A',1):10,('A',2):5,('A',3):1,
                       ('B',1):2, ('B',2):8,('B',3):4,
                       ('C',1):3, ('C',2):6}.get((var,val),0)

best_assign, best_sc = backtracking_csp(vars, doms, hard_cons, soft)
print(best_assign, best_sc)
