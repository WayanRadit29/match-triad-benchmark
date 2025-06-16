# src/ga/fitness.py
"""
Fitness module for Genetic Algorithm matching in Tutas.
"""

def time_score(student_time: str, tutor_time: str, fleksibel: bool) -> float:
    """
    Exact match scoring:
    - If student_time == tutor_time or fleksibel==True -> 1.0
    - Else -> 0.0
    """
    return 1.0 if student_time == tutor_time or fleksibel else 0.0


def score_pair(s, t, weights):
    """
    Compute weighted score for a student-tutor pair.
    s, t: dict or pandas.Series with keys:
        'mata_kuliah', 'subbab', 'gaya_belajar', 'mode',
        'waktu', 'fleksibilitas_waktu'
    weights: dict with weights for those keys.
    Returns:
        total weighted score (float),
        count of satisfied constraints (int)
    """
    # Check each constraint
    subj_match  = 1 if s['mata_kuliah'] == t['mata_kuliah'] else 0
    topic_match = 1 if s['subbab']       == t['subbab']       else 0
    style_match = 1 if s['gaya_belajar'] == t['gaya_belajar'] else 0
    mode_match  = 1 if s['mode']         == t['mode']         else 0

    fleks = bool(s.get('fleksibilitas_waktu', False))
    time_match = 1 if (s['waktu'] == t['waktu'] or fleks) else 0

    # Weighted score
    total = (
        weights['mata_kuliah']  * subj_match +
        weights['subbab']       * topic_match +
        weights['gaya_belajar'] * style_match +
        weights['mode']         * mode_match +
        weights['waktu']        * time_match
    )
    # Count of constraints
    satisfied_count = subj_match + topic_match + style_match + mode_match + time_match
    return total, satisfied_count


def compute_fitness(chromosome, df_students, df_tutors, weights):
    """
    chromosome: list of tutor_id per student_id
    df_students: pandas.DataFrame indexed by student ID
    df_tutors: pandas.DataFrame indexed by tutor ID
    weights: dict of metric weights

    Returns:
        dict with 'total_score' and 'pct_satisfied'
        where 'pct_satisfied' is the average percentage of constraints satisfied per pair.
    """
    total_score = 0.0
    total_pct = 0.0
    num_constraints = len(weights)  # e.g., 5
    n = len(chromosome)

    for stu_id, tut_id in enumerate(chromosome):
        s = df_students.loc[stu_id]
        t = df_tutors.loc[tut_id]
        sc, count_sat = score_pair(s, t, weights)
        total_score += sc
        # percentage of constraints satisfied for this pair
        total_pct += (count_sat / num_constraints)

    # average percentage across all pairs
    avg_pct_satisfied = total_pct / n if n > 0 else 0.0

    return {
        'total_score': total_score,
        'pct_satisfied': avg_pct_satisfied
    }
