"""
Modul fitness untuk algoritma genetika dan simulated annealing di sistem matching Tutas.
"""

def time_score(student_time: str, tutor_time: str, fleksibel: bool) -> float:
    """
    Skor waktu:
    - Kalau waktu cocok ATAU murid fleksibel → 1.0
    - Selain itu → 0.0
    """
    return 1.0 if student_time == tutor_time or fleksibel else 0.0

def score_pair(s, t, weights):
    """
    Hitung skor total dan jumlah constraint yang terpenuhi buat 1 pasangan murid-tutor.
    s,t: Series pandas dengan kolom:
        'mata_kuliah','subbab','gaya_belajar','mode','waktu','fleksibilitas_waktu'
    weights: dict bobot untuk tiap constraint.
    Return:
      - total skor (float)
      - jumlah constraint terpenuhi (int)
    """
    subj_match   = 1 if s['mata_kuliah'] == t['mata_kuliah'] else 0
    topic_match  = 1 if s['subbab']        == t['subbab']        else 0
    style_match  = 1 if s['gaya_belajar']  == t['gaya_belajar']  else 0
    mode_match   = 1 if s['mode']          == t['mode']          else 0
    fleks        = bool(s.get('fleksibilitas_waktu', False))
    time_match   = 1 if (s['waktu'] == t['waktu'] or fleks) else 0

    total = (
        weights['mata_kuliah']   * subj_match  +
        weights['subbab']        * topic_match +
        weights['gaya_belajar']  * style_match +
        weights['mode']          * mode_match  +
        weights['waktu']         * time_match
    )

    satisfied_count = subj_match + topic_match + style_match + mode_match + time_match
    return total, satisfied_count

def compute_fitness(chromosome, df_students, df_tutors, weights):
    """
    chromosome: list tutor_index per student_index
    df_students, df_tutors: DataFrame dengan index 0..n-1
    weights: dict bobot per constraint (jumlah kunci 5)

    Returns dict:
      - total_score   : float (jumlah skor semua pasangan)
      - pct_satisfied : float (rata-rata persentase constraint terpenuhi)
    """
    total_score = 0.0
    total_pct   = 0.0
    num_constraints = len(weights)    # misal 5
    n = len(chromosome)

    for stu_id, tut_id in enumerate(chromosome):
        s = df_students.loc[stu_id]
        t = df_tutors.loc[tut_id]
        sc, count_sat = score_pair(s, t, weights)
        total_score += sc
        total_pct   += (count_sat / num_constraints)

    avg_pct_satisfied = (total_pct / n) if n > 0 else 0.0
    return {
        'total_score': total_score,
        'pct_satisfied': avg_pct_satisfied
    }
