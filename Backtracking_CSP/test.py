import os
import time
import pandas as pd
import operator
from back_CSP import backtracking_csp
from fitness import score_pair

# Scenario configuration (keys match CSV filenames)
scenario_order = [
    'scenario1_fixed',
    'scenario 2_5_fixed',
    'scenario 2_10_fixed',
    'scenario 2_25_fixed',
    'scenario3_conflict_single_match'
]

# Descriptive titles for output
title_map = {
    'scenario1_fixed': 'Skenario 1 – Dataset Lengkap (10 pasang murid dan tutor)',
    'scenario 2_5_fixed': 'Skenario 2 – 5 Pasang Murid-Tutor',
    'scenario 2_10_fixed': 'Skenario 2 – 10 Pasang Murid-Tutor',
    'scenario 2_25_fixed': 'Skenario 2 – 25 Pasang Murid-Tutor',
    'scenario3_conflict_single_match': 'Skenario 3 – Konflik Preferensi'
}

# Weights for scoring, same as GA reference
default_weights = {
    'mata_kuliah':  0.3,
    'subbab':       0.2,
    'gaya_belajar': 0.2,
    'mode':         0.1,
    'waktu':        0.2
}

# Load preferences from CSV
def load_preferences(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()
    df['status'] = df['status'].str.lower()
    df_students = df[df['status'] == 'murid'].reset_index(drop=True)
    df_tutors   = df[df['status'] == 'tutor'].reset_index(drop=True)
    return df_students, df_tutors

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')

    print("\nBacktracking CSP + MRV")
    print("")

    for key in scenario_order:
        filename = f"{key}.csv"
        path = os.path.join(data_dir, filename)
        if not os.path.isfile(path):
            continue

        df_students, df_tutors = load_preferences(path)
        n_students = len(df_students)
        n_tutors   = len(df_tutors)

        variables = list(range(n_students))
        domains   = {i: list(range(n_tutors)) for i in variables}
        constraints = []  # allow reuse of tutors

        # Soft scoring function
        weights = default_weights
        def soft_score(var, val):
            s = df_students.loc[var]
            t = df_tutors.loc[val]
            total, _ = score_pair(s, t, weights)
            return total

        # Solve CSP
        t0 = time.perf_counter()
        assignment, total_score = backtracking_csp(
            variables, domains, constraints, soft_score
        )
        t1 = time.perf_counter()
        # Check determinism
        deterministic = all(
            backtracking_csp(variables, domains, constraints, soft_score)[1] == total_score
            for _ in range(2)
        )
        elapsed = t1 - t0

        # Calculate fulfillment: average satisfied metrics
        total_sat = 0.0
        num_metrics = len(default_weights)
        for var, val in assignment.items():
            _, sat = score_pair(df_students.loc[var], df_tutors.loc[val], weights)
            total_sat += sat / num_metrics
        pct_satisfied = (total_sat / n_students) if n_students else 0

        # Output results
        title = title_map.get(key, key)
        print(f"\n=== {title} ===")
        print("Best Assignment:")
        for var, val in assignment.items():
            stud = df_students.loc[var, 'nama']
            tut  = df_tutors.loc[val, 'nama']
            print(f" - {stud} → {tut} (score={soft_score(var,val):.2f})")
        best_assignment_list = [assignment.get(i, None) for i in range(n_students)]
        print(f"Best assignment (list format):\n{best_assignment_list}")
        print(f"Total score: {total_score:.2f}")
        print(f"Constraint fulfillment: {pct_satisfied:.2%}")
        print(f"Execution time: {elapsed:.4f} seconds")
        print(f"Deterministic: {deterministic}")