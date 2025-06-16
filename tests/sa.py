import random
import numpy as np

def sa_match(murid, tutor, cap_init, pref, T0=1.0, cooling=0.995, steps=1500):
    """
    Simulated Annealing for matching murid→tutor under capacity constraints.

    Args:
        murid (list): daftar ID murid
        tutor (list): daftar ID tutor
        cap_init (dict): kapasitas tiap tutor, e.g. {tutor_id: capacity}
        pref (dict): preferensi, key=(m,t), value=dict atribut→skor binary
        T0 (float): suhu awal
        cooling (float): faktor pendinginan per iterasi
        steps (int): jumlah iterasi

    Returns:
        best (dict): assignment terbaik {murid_id: tutor_id}
        best_fit (float): nilai fitness assignment terbaik c
    """ 
    # Precompute skor per pasangan
    score_pair = {(m,t): sum(pref[(m,t)].values()) for m in murid for t in tutor}
    PEN        = max(score_pair.values()) * len(murid)

    # Inisialisasi random assignment
    curr     = {m: random.choice(tutor) for m in murid}
    best     = curr.copy()
    best_fit = sum(score_pair[(m, curr[m])] for m in murid)

    def fitness(assign):
        s = sum(score_pair[(m, assign[m])] for m in murid)
        overflow = sum(
            max(0, sum(1 for x in assign if assign[x] == t) - cap_init[t])
            for t in tutor
        )
        return s - PEN * overflow

    T = T0
    for _ in range(steps):
        # Propose neighbor dengan mengganti satu murid acak
        child = curr.copy()
        m = random.choice(murid)
        child[m] = random.choice(tutor)

        f_child = fitness(child)
        f_curr  = fitness(curr)
        delta   = f_child - f_curr

        # Terima dengan Metropolis criterion
        if delta > 0 or random.random() < np.exp(delta / T):
            curr = child
            if f_child > best_fit:
                best_fit = f_child
                best     = child.copy()

        T *= cooling

    return best, best_fit
