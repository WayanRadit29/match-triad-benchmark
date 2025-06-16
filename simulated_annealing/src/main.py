"""
Main pipeline Simulated Annealing untuk matching Tutas:
- Otomatis baca folder 'data'
- Jalankan SA untuk tiap skenario (urut)
- Ukur metrik: kualitas solusi, waktu, pemenuhan constraint, determinisme
- Tampilkan hasil terbaik per skenario
"""
import pandas as pd
import os
import time
from sa import run_sa  # pastikan path sesuai

# mapping nama file ke judul skenario
title_map = {
    'scenario1_fixed': 'Skenario 1 – Dataset Lengkap (10 pasang murid dan tutor)',
    'scenario 2_5_fixed': 'Skenario 2 – Perbandingan Metode Matching (5 pasang murid & tutor)',
    'scenario 2_10_fixed': 'Skenario 2 – Perbandingan Metode Matching (10 pasang murid & tutor)',
    'scenario 2_25_fixed': 'Skenario 2 – Perbandingan Metode Matching (25 pasang murid & tutor)',
    'scenario3_conflict_heavy_fleksibel': 'Skenario 3 – Konflik Preferensi Tinggi (Satu Tutor Diperebutkan Banyak Murid)'
}

scenario_order = [
    'scenario1_fixed',
    'scenario 2_5_fixed',
    'scenario 2_10_fixed',
    'scenario 2_25_fixed',
    'scenario3_conflict_heavy_fleksibel'
]

def load_preferences(path: str):
    df = pd.read_csv(path, index_col=0)
    df['Status'] = df['Status'].str.lower()
    df_students = df[df['Status'] == 'murid'].drop(columns=['Status']).reset_index(drop=True)
    df_tutors = df[df['Status'] == 'tutor'].drop(columns=['Status']).reset_index(drop=True)
    return df_students, df_tutors

def run_scenario_sa(file_path: str, weights: dict, sa_params: dict):
    key = os.path.splitext(os.path.basename(file_path))[0]
    df_students, df_tutors = load_preferences(file_path)

    # Run SA sekali
    res0 = run_sa(df_students, df_tutors, weights, **sa_params)

    # Uji deterministik: run 3x dan bandingkan hasil
    res1 = run_sa(df_students, df_tutors, weights, **sa_params)
    res2 = run_sa(df_students, df_tutors, weights, **sa_params)
    deterministic = (
        res0['best_assignment'] == res1['best_assignment'] == res2['best_assignment'] and
        res0['best_fitness'] == res1['best_fitness'] == res2['best_fitness']
    )

    return {
        'scenario_key': key,
        'best_assignment': res0['best_assignment'],
        'best_fitness': res0['best_fitness'],
        'exec_time': res0['exec_time'],
        'deterministic': deterministic
    }

def run_all_scenarios():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, 'data')

    if not os.path.isdir(data_dir):
        print(f"Folder data ga ketemu di {data_dir}")
        return

    weights = {'mata_kuliah': 0.3, 'subbab': 0.2, 'gaya_belajar': 0.2, 'mode': 0.1, 'waktu': 0.2}
    sa_params = {'T0': 1.0, 'cooling': 0.995, 'steps': 1000}

    for key in scenario_order:
        file_name = f"{key}.csv"
        fpath = os.path.join(data_dir, file_name)
        if not os.path.isfile(fpath):
            continue

        res = run_scenario_sa(fpath, weights, sa_params)
        title = title_map.get(res['scenario_key'], res['scenario_key'])
        bf = res['best_fitness']

        print(f"\n=== {title} ===")
        print("Best Assignment:", res['best_assignment'])
        print(f"Total score: {bf['total_score']:.2f}")
        print(f"Constraint fulfillment: {bf['pct_satisfied']:.2%}")
        print(f"Execution time: {res['exec_time']:.4f} seconds")
        print(f"Deterministic: {res['deterministic']}")

if __name__ == "__main__":
    run_all_scenarios()
