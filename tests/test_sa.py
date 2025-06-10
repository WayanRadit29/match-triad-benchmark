import random
import time
import numpy as np
import pandas as pd

# Utilities: Generate Preferences & Scenarios
def generate_preferences(murid, tutor, mode="random", popular_subset=None, weights=None):
    attrs = ["waktu","topik","mode","gaya"]
    pref = {}
    for m in murid:
        if mode == "conflict":
            t_good = random.choice(tutor)
            for t in tutor:
                pref[(m,t)] = {a: (1 if t == t_good else 0) for a in attrs}
        else:
            for t in tutor:
                pref[(m,t)] = {a: random.randint(0,1) for a in attrs}
        if weights:
            for t in tutor:
                for a in attrs:
                    pref[(m,t)][a] *= weights.get(a,1)
    return pref

def scenario_conflict_heavy(n_m, n_t):
    murid = list(range(n_m))
    tutor = list(range(n_t))
    cap = {t:1 for t in tutor}
    pref = generate_preferences(murid, tutor, mode="conflict")
    return murid, tutor, cap, pref

def scenario_capacity(n_m, n_t, asym=False):
    murid = list(range(n_m))
    tutor = list(range(n_t))
    if asym:
        cap = {t:(5 if t<2 else 1) for t in tutor}
    else:
        cap = {t: max(1, n_m//n_t) for t in tutor}
    pref = generate_preferences(murid, tutor, mode="random")
    return murid, tutor, cap, pref

# Simulated Annealing
def sa_match(murid, tutor, cap_init, pref, T0=1.0, cooling=0.995, steps=2000):
    score_pair = {(m,t): sum(pref[(m,t)].values()) for m in murid for t in tutor}
    PEN = max(score_pair.values()) * len(murid)

    curr = {m: random.choice(tutor) for m in murid}
    def fitness(assign):
        s = sum(score_pair[(m,assign[m])] for m in murid)
        overflow = sum(max(0, sum(1 for x in assign if assign[x]==t)-cap_init[t]) for t in tutor)
        return s - PEN*overflow

    best, best_fit = curr.copy(), fitness(curr)
    T = T0
    for _ in range(steps):
        child = curr.copy()
        m = random.choice(murid)
        child[m] = random.choice(tutor)
        f_child, f_curr = fitness(child), fitness(curr)
        delta = f_child - f_curr
        if delta > 0 or random.random() < np.exp(delta/T):
            curr = child
            if f_child > best_fit:
                best, best_fit = child.copy(), f_child
        T *= cooling

    return best, best_fit

# Evaluasi
def evaluate(assign, pref, cap):
    if not assign:
        return 0, 0.0
    total_attr = len(assign) * 4
    match_score = sum(sum(pref[(m,assign[m])].values()) for m in assign)
    percent = match_score / total_attr * 100
    return match_score, percent

# Runner khusus SA
def run_sa_only(scenarios, repeat=3, **sa_kwargs):
    records = []
    for name, (murid, tutor, cap, pref) in scenarios.items():
        for _ in range(repeat):
            t0 = time.perf_counter()
            sol_sa, _ = sa_match(murid, tutor, cap, pref, **sa_kwargs)
            t1 = time.perf_counter()
            score, pct = evaluate(sol_sa, pref, cap)
            records.append({
                "Scenario": name,
                "Alg": "SA",
                "Score": score,
                "%Constraint": round(pct,2),
                "Time(s)": round(t1-t0,6)
            })
    return pd.DataFrame(records)

if __name__ == "__main__":
    # Definisikan skenario
    scenarios = {
        "Conflict-Heavy": scenario_conflict_heavy(15, 5),
        "Capacity-Sym":   scenario_capacity(10, 10, asym=False),
        "Capacity-Asym":  scenario_capacity(10, 10, asym=True),
    }

    # Jalankan SA dengan parameter default (T0, cooling, steps)
    df_sa = run_sa_only(scenarios, repeat=5, T0=1.0, cooling=0.995, steps=1500)

    # Tampilkan hasil
    summary = df_sa.groupby("Scenario")[["Score","%Constraint","Time(s)"]].agg(['mean','std']).round(3)
    print("\n=== Hasil SA-only ===\n", df_sa.to_string(index=False))
    print("\n=== Ringkasan SA-only (μ ± σ) ===\n", summary)
