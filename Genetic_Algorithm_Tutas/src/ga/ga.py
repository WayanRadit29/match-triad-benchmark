"""
Algoritma Genetika untuk matching murid-tutor di Tutas.
Ngatur: inisialisasi populasi, seleksi, crossover, mutasi, dan loop GA.
"""
import random
from typing import List, Dict, Any
from ga.chromosome import init_chromosome
from ga.fitness import compute_fitness

def init_population(pop_size:int,num_pairs:int)->List[List[int]]:
    #generate_populasi_awal_sebanyak_pop_size
    return [init_chromosome(num_pairs) for _ in range(pop_size)]

def tournament_selection(pop:List[List[int]],fitnesses:List[Dict[str,Any]],k:int=3)->List[int]:
    #ambil_k_kromosom_acak_dan_pilih_yang_total_score_tertinggi
    selected=random.sample(list(zip(pop,fitnesses)),k)
    parent=max(selected,key=lambda pair:pair[1]['total_score'])[0]
    return parent

def pmx_crossover(parent1:List[int],parent2:List[int])->List[int]:
    #Partially_Mapped_Crossover_untuk_permutesi_kromosom
    size=len(parent1)
    c1,c2=parent1[:],parent2[:]
    a,b=sorted(random.sample(range(size),2))
    mapping1={c1[i]:c2[i] for i in range(a,b+1)}
    child=[-1]*size
    child[a:b+1]=c1[a:b+1]
    for i in list(range(0,a))+list(range(b+1,size)):
        gene=c2[i]
        while gene in mapping1:
            gene=mapping1[gene]
        child[i]=gene
    return child

def swap_mutation(chrom:List[int],mutation_rate:float)->List[int]:
    #swap_dua_posisi_dengan_probabilitas_tertentu
    child=chrom[:]
    if random.random()<mutation_rate:
        i,j=random.sample(range(len(child)),2)
        child[i],child[j]=child[j],child[i]
    return child

def run_ga(df_students,df_tutors,
           weights:Dict[str,float],
           pop_size:int=50,
           generations:int=100,
           crossover_rate:float=0.8,
           mutation_rate:float=0.1)->Dict[str,Any]:
    """
    Main_loop_algoritma_genetika
    Output: best_chromosome dan best_fitness-nya
    """
    num_pairs=len(df_students)
    population=init_population(pop_size,num_pairs)
    fitnesses=[compute_fitness(ch,df_students,df_tutors,weights) for ch in population]
    best=max(zip(population,fitnesses),key=lambda p:p[1]['total_score'])

    for gen in range(generations):
        new_pop=[]
        #elitism:bawa_solusi_terbaik_ke_generasi_selanjutnya
        new_pop.append(best[0])
        while len(new_pop)<pop_size:
            parent1=tournament_selection(population,fitnesses)
            parent2=tournament_selection(population,fitnesses)
            if random.random()<crossover_rate:
                child=pmx_crossover(parent1,parent2)
            else:
                child=parent1[:]
            child=swap_mutation(child,mutation_rate)
            new_pop.append(child)
        population=new_pop
        fitnesses=[compute_fitness(ch,df_students,df_tutors,weights) for ch in population]
        current_best=max(zip(population,fitnesses),key=lambda p:p[1]['total_score'])
        if current_best[1]['total_score']>best[1]['total_score']:
            best=current_best

    return {'best_chromosome':best[0],'best_fitness':best[1]}
