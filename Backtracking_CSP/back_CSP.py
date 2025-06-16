import copy
from typing import Any, Callable, Dict, List, Tuple

def backtracking_csp(
    variables: List[Any],
    domains: Dict[Any, List[Any]],
    constraints: List[Tuple[Any, Any, Callable[[Any, Any], bool]]],
    soft_score: Callable[[Any, Any], float]
) -> Tuple[Dict[Any, Any], float]:
    """
    Backtracking CSP with MRV, forward-checking, value ordering, and branch-and-bound.
    """
    # Initialize
    init_domains = {v: list(domains.get(v, [])) for v in variables}
    best_assignment: Dict[Any, Any] = {}
    best_score: float = float('-inf')

    def mrv(curr_domains: Dict[Any, List[Any]], assignment: Dict[Any, Any]) -> Any:
        unassigned = [v for v in variables if v not in assignment]
        return min(unassigned, key=lambda v: len(curr_domains[v]))

    def forward_check(var: Any, val: Any, curr_domains: Dict[Any, List[Any]], assignment: Dict[Any, Any]) -> Dict[Any, List[Any]]:
        new_domains = copy.deepcopy(curr_domains)
        for (X, Y, cons) in constraints:
            if X == var and Y not in assignment:
                new_domains[Y] = [w for w in new_domains[Y] if cons(val, w)]
            if Y == var and X not in assignment:
                new_domains[X] = [w for w in new_domains[X] if cons(w, val)]
        return new_domains

    def backtrack(assignment: Dict[Any, Any], curr_domains: Dict[Any, List[Any]], curr_score: float) -> None:
        nonlocal best_score, best_assignment
        # Compute optimistic bound on remaining
        unassigned = [v for v in variables if v not in assignment]
        rem_upper = 0.0
        for v in unassigned:
            if curr_domains[v]:
                rem_upper += max(soft_score(v, val) for val in curr_domains[v])
        if curr_score + rem_upper <= best_score:
            return
        # If complete, record
        if not unassigned:
            if curr_score > best_score:
                best_score = curr_score
                best_assignment = assignment.copy()
            return
        # Select var via MRV
        var = mrv(curr_domains, assignment)
        # Order values by descending soft_score
        vals = sorted(curr_domains[var], key=lambda x: soft_score(var, x), reverse=True)
        for val in vals:
            # Check binary constraints with assigned vars
            consistent = True
            for (X, Y, cons) in constraints:
                if X == var and Y in assignment and not cons(val, assignment[Y]):
                    consistent = False; break
                if Y == var and X in assignment and not cons(assignment[X], val):
                    consistent = False; break
            if not consistent:
                continue
            # Assign and recurse
            assignment[var] = val
            new_score = curr_score + soft_score(var, val)
            pruned = forward_check(var, val, curr_domains, assignment)
            if all(pruned[w] for w in variables if w not in assignment):
                backtrack(assignment, pruned, new_score)
            del assignment[var]

    # Start backtracking
    backtrack({}, init_domains, 0.0)
    return best_assignment, best_score