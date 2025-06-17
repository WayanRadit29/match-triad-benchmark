# MATCH-TRIAD-BENCHMARK: Student-Tutor Matching with CSP, Genetic Algorithm, and Simulated Annealing

## Project Description

This repository is a benchmark suite designed to compare three algorithmic approaches for solving the student-tutor matching problem based on individual preferences.

The objective is to analyze and contrast the strengths and trade-offs of:

* **Backtracking CSP + MRV + Forward Checking** – an exact, deterministic method rooted in classical constraint satisfaction.
* **Genetic Algorithm (GA)** – a stochastic, population-based metaheuristic inspired by biological evolution.
* **Simulated Annealing (SA)** – a probabilistic optimization strategy modeled on the annealing process in metallurgy.

Each algorithm is evaluated across a series of structured scenarios using consistent metrics: total score (solution quality), percentage of satisfied constraints, runtime performance, and consistency (determinism) of outcomes.

## Folder Structure

```
match-triad-benchmark/
├── Backtracking_CSP/
│   ├── back_CSP.py       # CSP + MRV implementation
│   ├── fitness.py        # Suitability scoring function
│   └── test.py           # CSP main runner
│
├── Genetic_Algorithm/
│   └── src/
│       ├── ga/           # GA implementation
│       ├── fitness.py    # Fitness function for GA
│       └── main.py       # GA scenario pipeline
│
├── simulated_annealing/
│   └── src/
│       ├── sa.py         # SA implementation
│       ├── fitness.py    # Fitness function for SA
│       └── main.py       # SA scenario pipeline
│
├── data/                 # CSV datasets for all scenarios
└── README.md
```

## Testing Scenarios

### S1 – Complete Dataset (10 students & 10 tutors)

* Fully filled preference profiles
* Each tutor only accepts 1 student

### S2 – Scalable Benchmark (5, 10, 25 pairs)

* Varied and realistic preferences
* Used to test algorithm scalability & efficiency

### S3 – Conflict-Heavy Matching

* Only 2–3 popular tutors
* All students compete for limited tutor resources

---

## Implemented Methods

### Backtracking CSP + MRV + Forward Checking

* Deterministic (always same result)
* Accurate but time-consuming on large scale

### Genetic Algorithm

* Chromosome: list of tutor indices
* Fitness: weighted combination of attributes (subject, topic, learning style, etc.)
* Operators: crossover, mutation, selection

### Simulated Annealing

* Representation: assignment list
* Accepts worse solutions early on (probabilistic)
* Fast and efficient for larger scenarios

---

## Summary of Experimental Results

| Scenario | Algorithm | Total Score | Constraint (%) | Execution Time | Deterministic |
| -------- | --------- | ----------- | -------------- | -------------- | ------------- |
| S1 (10)  | CSP       | 7.80        | **70.00%**     | 0.39s          | ✅             |
|          | GA        | 7.30        | 68.00%         | 2.33s          | ✅             |
|          | SA        | 7.40        | 70.00%         | **0.47s**      | ❌             |
| S2 (5)   | CSP       | 2.40        | **52.00%**     | 0.37s          | ✅             |
|          | GA        | 2.30        | 52.00%         | 1.12s          | ✅             |
|          | SA        | 2.50        | 48.00%         | **0.23s**      | ❌             |
| S2 (10)  | CSP       | 5.80        | **52.00%**     | 2.03s          | ✅             |
|          | GA        | 5.00        | 48.00%         | 2.22s          | ❌             |
|          | SA        | 5.80        | 54.00%         | **0.46s**      | ❌             |
| S2 (25)  | CSP       | **17.60**   | **66.60%**     | 9.14s          | ✅             |
|          | GA        | 13.20       | 51.20%         | 5.45s          | ❌             |
|          | SA        | 16.20       | 62.40%         | **1.14s**      | ❌             |
| S3       | CSP       | 7.80        | 68.00%         | 0.41s          | ✅             |
|          | GA        | 2.70        | 26.00%         | 2.26s          | ❌             |
|          | SA        | **7.80**    | **68.00%**     | **0.45s**      | ✅             |

---

## Visualizations

### Total Score & Constraint Fulfillment

![Score & Constraint](assets/Screenshot%202025-06-17%20153127.png)
![Score & Constraint](assets/Screenshot%202025-06-17%20153135.png)

### Execution Time per Scenario

![Execution Time](assets/Screenshot%202025-06-17%20153144.png)

### Determinism Heatmap

![Determinism](assets/Screenshot%202025-06-17%20153153.png)

## ⚒ Requirements

```bash
pip install -r requirements.txt
```

## ▶ How to Run

```bash
# Backtracking CSP
cd Backtracking_CSP
python test.py

# Genetic Algorithm
cd Genetic_Algorithm/src
python main.py

# Simulated Annealing
cd simulated_annealing/src
python main.py
```

---

## Notes

* Datasets are provided in the `/data/` folder
* Results and plots can be used in reports & presentations
* Full evaluation includes score, constraint fulfillment, time, and determinism

---

> ⭐️ If you find this useful, please star the repo!

---

MIT License © 2025
