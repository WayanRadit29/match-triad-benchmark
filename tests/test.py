import random
import time
import numpy as np
import pandas as pd
import statistics

# 1. Utilities: Generate Preferences & Scenarios

def generate_preferences(murid, tutor, mode="random", popular_subset=None, weights=None):
    attrs = ["waktu","topik","mode","gaya"]
    pref = {}
    for m in murid:
        if mode == "conflict":
            # Setiap murid hanya cocok dengan satu tutor random
            t_good = random.choice(tutor)
            for t in tutor:
                pref[(m,t)] = {a: (1 if t == t_good else 0) for a in attrs}
        elif mode == "popular":
            # Hanya tutor dalam popular_subset yang cocok
            for t in tutor:
                ok = (t in popular_subset)
                pref[(m,t)] = {a: (1 if ok else 0) for a in attrs}
        else:
            # Random binary untuk tiap atribut
            for t in tutor:
                pref[(m,t)] = {a: random.randint(0,1) for a in attrs}
        # Apply weights jika disediakan
        if weights:
            for t in tutor:
                for a in attrs:
                    pref[(m,t)][a] *= weights.get(a,1)
    return pref

def scenario_conflict_heavy(n_m, n_t):
    murid = list(range(n_m))
    tutor = list(range(n_t))
    # Kapasitas 1 → paksa 1-on-1, banyak konflik
    cap = {t:1 for t in tutor}
    pref = generate_preferences(murid, tutor, mode="conflict")
    return murid, tutor, cap, pref

def scenario_capacity(n_m, n_t, asym=False):
    murid = list(range(n_m))
    tutor = list(range(n_t))
    if asym:
        # 2 tutor populer kapasitas 5, sisanya 1
        cap = {t:(5 if t<2 else 1) for t in tutor}
    else:
        # Distribusi merata
        cap = {t: max(1, n_m//n_t) for t in tutor}
    pref = generate_preferences(murid, tutor, mode="random")
    return murid, tutor, cap, pref

# 2. CSP Backtracking + MRV + Forward Checking

def csp_backtrack(murid, tutor, cap_init, pref):
    # Precompute skor per (murid,tutor)
    score_pair = {(m,t): sum(pref[(m,t)].values()) for m in murid for t in tutor}
    best = {"assign": {}, "score": -1}

    def mrv(domains):
        # Pilih variabel dengan domain terkecil
        return min((v for v in domains if domains[v]), key=lambda v: len(domains[v]), default=None)

    def backtrack(assignment, domains, cap, curr_score):
        # Base case: semua murid terassign
        if len(assignment) == len(murid):
            if curr_score > best["score"]:
                best["assign"] = assignment.copy()
                best["score"] = curr_score
            return

        var = mrv(domains)
        if var is None:
            return

        for t in list(domains[var]):
            if cap[t] > 0:
                # Simpan state
                cap[t] -= 1
                old_domains = {v: domains[v][:] for v in domains}
                # Forward checking
                if cap[t] == 0:
                    for v in domains:
                        if v != var and t in domains[v]:
                            domains[v].remove(t)
                # Assign & recuse
                assignment[var] = t
                backtrack(assignment, domains, cap, curr_score + score_pair[(var, t)])
                # Revert state
                assignment.pop(var, None)
                domains = old_domains
                cap[t] += 1

    domains = {m: tutor[:] for m in murid}
    backtrack({}, domains, cap_init.copy(), 0)
    return best["assign"], best["score"]

# 3. Simulated Annealing

def sa_match(murid, tutor, cap_init, pref, T0=1.0, cooling=0.995, steps=2000):
    score_pair = {(m,t): sum(pref[(m,t)].values()) for m in murid for t in tutor}
    PEN = max(score_pair.values()) * len(murid)

    # Inisialisasi random
    curr = {m: random.choice(tutor) for m in murid}
    def fitness(assign):
        # Skor minus penalti overflow kapasitas
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

# 4. Genetic Algorithm

def ga_match(murid, tutor, cap_init, pref,
             pop_size=30, gens=80, cross_p=0.8, mut_p=0.1):
    score_pair = {(m,t): sum(pref[(m,t)].values()) for m in murid for t in tutor}
    PEN = max(score_pair.values()) * len(murid)

    def fitness(chromo):
        s = sum(score_pair[(i,chromo[i])] for i in range(len(murid)))
        overflow = sum(max(0,
               sum(1 for x,a in enumerate(chromo) if a==t)-cap_init[t])
               for t in tutor)
        return s - PEN*overflow

    # Inisiasi populasi
    pop = [[random.choice(tutor) for _ in murid] for _ in range(pop_size)]
    for _ in range(gens):
        pop = sorted(pop, key=lambda c: fitness(c), reverse=True)
        new_pop = pop[:2]
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(pop[:10], 2)
            if random.random() < cross_p:
                cp = random.randint(1, len(murid)-1)
                c1 = p1[:cp] + p2[cp:]
                c2 = p2[:cp] + p1[cp:]
            else:
                c1, c2 = p1[:], p2[:]
            # Mutasi
            for c in (c1, c2):
                if random.random() < mut_p:
                    idx = random.randrange(len(murid))
                    c[idx] = random.choice(tutor)
            new_pop += [c1, c2]
        pop = new_pop[:pop_size]

    best = max(pop, key=fitness)
    return {m: best[i] for i,m in enumerate(murid)}, fitness(best)

# 5. Evaluasi & Runner

def evaluate(assign, pref, cap):
    if not assign:
        return 0, 0.0
    total_attr = len(assign) * 4
    match_score = sum(sum(pref[(m,assign[m])].values()) for m in assign)
    percent = match_score / total_attr * 100
    return match_score, percent

def run_scenario(scenario_args, repeat=3):
    records = []
    murid, tutor, cap, pref = scenario_args
    for _ in range(repeat):
        t0 = time.perf_counter(); sol_csp, _ = csp_backtrack(murid,tutor,cap,pref); t1 = time.perf_counter()
        m1,_pct1 = evaluate(sol_csp, pref, cap)
        t2 = time.perf_counter(); sol_sa, _ = sa_match(murid,tutor,cap,pref); t3 = time.perf_counter()
        m2,_pct2 = evaluate(sol_sa, pref, cap)
        t4 = time.perf_counter(); sol_ga, _ = ga_match(murid,tutor,cap,pref); t5 = time.perf_counter()
        m3,_pct3 = evaluate(sol_ga, pref, cap)

        for alg, score, t_start, t_end in [
            ("CSP", m1, t0, t1),
            ("SA",  m2, t2, t3),
            ("GA",  m3, t4, t5),
        ]:
            records.append({
                "Alg": alg,
                "Score": score,
                "%Constraint": round((score/(len(murid)*4))*100,2),
                "Time(s)": round(t_end - t_start, 6)
            })
    return pd.DataFrame(records)

if __name__ == "__main__":
    scenarios = {
        "Conflict-Heavy": scenario_conflict_heavy(15, 5),
        "Capacity-Sym":   scenario_capacity(20,10,asym=False),
        "Capacity-Asym":  scenario_capacity(20,10,asym=True),
    }

    results = []
    for name, sc in scenarios.items():
        df = run_scenario(sc, repeat=3)
        df["Scenario"] = name
        results.append(df)

    final = pd.concat(results, ignore_index=True)
    # Group dan ringkasan
    summary = final.groupby(["Scenario","Alg"])[["Score","%Constraint","Time(s)"]].mean()
    print("\n=== Ringkasan Hasil Perbandingan ===\n", summary)
