"""
Main pipeline algoritma genetika untuk matching Tutas:
- Otomatis baca folder 'data'
- Jalankan GA untuk tiap skenario (urut)
- Ukur metrik: kualitas solusi, waktu, pemenuhan constraint, determinisme
- Tampilkan hasil terbaik per skenario
"""
import pandas as pd
import os
import time
from ga.ga import run_ga

#mapping_nama_file_ke_judul_skenario
title_map={
    'scenario1_fixed':'Skenario 1 – Dataset Lengkap (10 pasang murid dan tutor)',
    'scenario 2_5_fixed':'Skenario 2 – Perbandingan Metode Matching (5 pasang murid & tutor)',
    'scenario 2_10_fixed':'Skenario 2 – Perbandingan Metode Matching (10 pasang murid & tutor)',
    'scenario 2_25_fixed':'Skenario 2 – Perbandingan Metode Matching (25 pasang murid & tutor)',
    'scenario3_conflict_heavy_fleksibel':'Skenario 3 – Konflik Preferensi Tinggi (Satu Tutor Diperebutkan Banyak Murid)'
}

#urutan_skenario_yang_dijalankan
scenario_order=[
    'scenario1_fixed',
    'scenario 2_5_fixed',
    'scenario 2_10_fixed',
    'scenario 2_25_fixed',
    'scenario3_conflict_heavy_fleksibel'
]

def load_preferences(path:str):
    #baca_csv_lalu_pisahkan_murid_dan_tutor
    df=pd.read_csv(path,index_col=0)
    df['Status']=df['Status'].str.lower()
    df_students=(df[df['Status']=='murid'].drop(columns=['Status']).reset_index(drop=True))
    df_tutors=(df[df['Status']=='tutor'].drop(columns=['Status']).reset_index(drop=True))
    return df_students,df_tutors

def run_scenario(file_path:str,weights:dict,ga_params:dict):
    #eksekusi_GA_untuk_satu_file_skenario
    key=os.path.splitext(os.path.basename(file_path))[0]
    df_students,df_tutors=load_preferences(file_path)

    start=time.perf_counter()
    r0=run_ga(df_students,df_tutors,weights,**ga_params)
    exec_time=time.perf_counter()-start

    #cek_deterministik_dengan_run_3_kali
    r1=run_ga(df_students,df_tutors,weights,**ga_params)
    r2=run_ga(df_students,df_tutors,weights,**ga_params)
    deterministic=(r0['best_chromosome']==r1['best_chromosome']==r2['best_chromosome'] and
                   r0['best_fitness']==r1['best_fitness']==r2['best_fitness'])

    return {
        'scenario_key':key,
        'best_chromosome':r0['best_chromosome'],
        'best_fitness':r0['best_fitness'],
        'exec_time':exec_time,
        'deterministic':deterministic
    }

def run_all_scenarios():
    #cari_folder_data
    script_dir=os.path.dirname(os.path.abspath(__file__))
    project_root=os.path.dirname(script_dir)
    data_dir=os.path.join(project_root,'data')

    if not os.path.isdir(data_dir):
        print(f"Folder data ga ketemu di {data_dir}")
        return

    #bobot_penilaian_dan_parameter_GA
    weights={'mata_kuliah':0.3,'subbab':0.2,'gaya_belajar':0.2,'mode':0.1,'waktu':0.2}
    ga_params={'pop_size':50,'generations':100,'crossover_rate':0.8,'mutation_rate':0.1}

    #loop_semua_skenario_dengan_urutan
    for key in scenario_order:
        file_name=f"{key}.csv"
        fpath=os.path.join(data_dir,file_name)
        if not os.path.isfile(fpath):
            continue

        res=run_scenario(fpath,weights,ga_params)
        title=title_map.get(res['scenario_key'],res['scenario_key'])
        bf=res['best_fitness']

        print(f"\n=== {title} ===")
        print("Best Chromosome:",res['best_chromosome'])
        print(f"Total score: {bf['total_score']:.2f}")
        print(f"Constraint fulfillment: {bf['pct_satisfied']:.2%}")
        print(f"Execution time: {res['exec_time']:.4f} seconds")
        print(f"Deterministic: {res['deterministic']}")

if __name__=="__main__":
    run_all_scenarios()
