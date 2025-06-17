# 📚 MATCH-TUTOR: Matching Murid dan Tutor dengan CSP, Genetic Algorithm, dan Simulated Annealing

## 🧠 Deskripsi Proyek

MATCH-TUTOR adalah sistem pencocokan otomatis antara murid dan tutor berbasis preferensi, menggunakan tiga pendekatan algoritmik:

* **Backtracking CSP + MRV + Forward Checking**
* **Genetic Algorithm (GA)**
* **Simulated Annealing (SA)**

Setiap metode dievaluasi berdasarkan: kualitas solusi (total score), pemenuhan constraint, waktu eksekusi, dan determinisme solusi.

## 📁 Struktur Folder

```
MATCH-TUTOR/
├── Backtracking_CSP/
│   ├── back_CSP.py       # Implementasi CSP + MRV
│   ├── fitness.py        # Fungsi evaluasi kesesuaian
│   └── test.py           # Main runner untuk CSP
│
├── Genetic_Algorithm/
│   └── src/
│       ├── ga/           # Implementasi GA
│       ├── fitness.py    # Fitness function untuk GA
│       └── main.py       # Pipeline GA untuk semua skenario
│
├── simulated_annealing/
│   └── src/
│       ├── sa.py         # Implementasi SA
│       ├── fitness.py    # Fitness function untuk SA
│       └── main.py       # Pipeline SA untuk semua skenario
│
├── data/                 # Dataset CSV untuk semua skenario
└── README.md
```

## 📊 Skenario Pengujian

### S1 – Dataset Lengkap (10 murid & 10 tutor)

* Preferensi lengkap
* 1 tutor hanya menerima 1 murid

### S2 – Skala Bertahap (5, 10, 25 pasangan)

* Preferensi bervariasi & realistis
* Digunakan untuk menguji efisiensi dan skalabilitas

### S3 – Conflict-Heavy Matching

* Tutor populer hanya 2-3 orang
* Semua murid bersaing terhadap tutor yang sama

---

## ⚙️ Metode yang Diimplementasikan

### ✅ Backtracking CSP + MRV + Forward Checking

* Deterministik (selalu hasil sama)
* Akurat, tapi boros waktu saat skenario besar

### ✅ Genetic Algorithm

* Representasi kromosom: list indeks tutor
* Evaluasi fitness: kombinasi bobot atribut (mata kuliah, topik, gaya belajar, dll)
* Operator: crossover, mutasi, seleksi

### ✅ Simulated Annealing

* Representasi solusi: assignment list
* Menerima solusi lebih buruk di awal (probabilistik)
* Cepat, cocok untuk skenario besar

---

## 📈 Hasil Eksperimen Ringkas

| Skenario | Algoritma | Total Skor | Constraint (%) | Waktu Eksekusi | Deterministik |
| -------- | --------- | ---------- | -------------- | -------------- | ------------- |
| S1 (10)  | CSP       | 7.80       | **70.00%**     | 0.39s          | ✅             |
|          | GA        | 7.30       | 68.00%         | 2.33s          | ✅             |
|          | SA        | 7.40       | 70.00%         | **0.47s**      | ❌             |
| S2 (5)   | CSP       | 2.40       | **52.00%**     | 0.37s          | ✅             |
|          | GA        | 2.30       | 52.00%         | 1.12s          | ✅             |
|          | SA        | 2.50       | 48.00%         | **0.23s**      | ❌             |
| S2 (25)  | CSP       | **17.60**  | **66.60%**     | 9.14s          | ✅             |
|          | GA        | 13.20      | 51.20%         | 5.45s          | ❌             |
|          | SA        | 16.20      | 62.40%         | **1.14s**      | ❌             |
| S3       | CSP       | 7.80       | 68.00%         | 0.41s          | ✅             |
|          | GA        | 2.70       | 26.00%         | 2.26s          | ❌             |
|          | SA        | **7.80**   | **68.00%**     | **0.45s**      | ✅             |

---

## 📌 Visualisasi

* **Bar Chart**: Perbandingan skor total dan persentase constraint antar metode

![Deskripsi Alt Text](assets\Screenshot 2025-06-17 153127.png)
![Deskripsi Alt Text](assets\Screenshot 2025-06-17 153135.png)

* **Line Plot**: Waktu eksekusi terhadap skenario (terlihat SA paling ringan)

![Deskripsi Alt Text](assets\Screenshot 2025-06-17 153144.png)

* **Heatmap**: Determinisme hasil (CSP selalu deterministik)

![Deskripsi Alt Text](assets\Screenshot 2025-06-17 153153.png)

## 🧪 Requirement

```bash
pip install -r requirements.txt
```

## ▶️ Cara Menjalankan

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

## 📌 Catatan

* Dataset sudah tersedia di folder `/data/`
* Hasil eksperimen dan plot dapat digunakan untuk laporan & presentasi
* Evaluasi lengkap mencakup *score, fulfillment, time, determinisme*

---

> ⭐️ If you find this useful, please star the repo!

---

MIT License © 2025
