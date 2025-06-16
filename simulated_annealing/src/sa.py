# sa.py

import random
import time
import numpy as np
from fitness import compute_fitness

def run_sa(df_students, df_tutors, weights,
           T0: float = 1.0,
           cooling: float = 0.995,
           steps: int = 1000):
    """
    Simulated Annealing untuk matching murid→tutor.

    Args:
        df_students: pd.DataFrame, index 0..n-1
        df_tutors  : pd.DataFrame, index 0..m-1
        weights    : dict, bobot per constraint
        T0         : suhu awal
        cooling    : faktor pendinginan per iterasi
        steps      : jumlah iterasi

    Returns:
        {
          'best_assignment': List[int],  # tutor index per student index
          'best_fitness'   : {'total_score':…, 'pct_satisfied':…},
          'exec_time'      : float,      # detik
          'deterministic'  : False
        }
    """
    n = len(df_students)
    m = len(df_tutors)

    # Inisialisasi acak
    curr = [random.randrange(m) for _ in range(n)]
    fit_curr = compute_fitness(curr, df_students, df_tutors, weights)
    best = curr.copy()
    best_fit = fit_curr.copy()

    T = T0
    start = time.perf_counter()
    for _ in range(steps):
        i = random.randrange(n)
        child = curr.copy()
        child[i] = random.randrange(m)

        fit_child = compute_fitness(child, df_students, df_tutors, weights)
        delta = fit_child['total_score'] - fit_curr['total_score']

        # Metropolis criterion
        if delta > 0 or random.random() < np.exp(delta / T):
            curr = child
            fit_curr = fit_child
            if fit_child['total_score'] > best_fit['total_score']:
                best = child.copy()
                best_fit = fit_child.copy()

        T *= cooling

    exec_time = time.perf_counter() - start
    return {
        'best_assignment': best,
        'best_fitness'   : best_fit,
        'exec_time'      : exec_time,
        'deterministic'  : False
    }
