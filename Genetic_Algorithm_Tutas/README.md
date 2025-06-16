# 💡 Sistem Matching Tutor-Murid dengan Algoritma Genetika

Proyek ini dikembangkan sebagai bagian dari Final Project mata kuliah **Konsep Kecerdasan Artifisial (KKA)**. Sistem ini bertujuan mencocokkan murid dengan tutor berdasarkan preferensi seperti:
- Mata kuliah
- Topik/subbab
- Waktu belajar
- Gaya belajar
- Metode belajar

Algoritma yang digunakan adalah **Genetic Algorithm (GA)** dengan penyesuaian untuk domain matching 1-on-1.

---

## 🛠 Teknologi & Library

- Python 3.12
- `pandas`, `numpy` – manipulasi data
- `matplotlib`, `networkx` *(opsional: untuk visualisasi)*

## 📁 Struktur Folder
.
├── data/ # Dataset skenario (.csv)
├── src/
│ └── ga/ # Kode utama algoritma GA
│ ├── chromosome.py # Representasi solusi
│ ├── fitness.py # Fungsi penilaian (fitness)
│ ├── ga.py # Proses seleksi, crossover, mutasi
│ └── main.py # Pipeline utama untuk semua skenario
├── requirements.txt # Library yang dibutuhkan
└── README.md # Deskripsi proyek

## ▶️ Cara Menjalankan
1. **Aktifkan virtual environment**  
   ```bash
   fpkka\Scripts\activate

2. Install dependensi
pip install -r requirements.txt

3. Jalankan Program
python src/ga/main.py

## 📊 Parameter Evaluasi

| **Metrik**               | **Penjelasan**                                                                 |
|--------------------------|--------------------------------------------------------------------------------|
| **Skor Total**           | Jumlah skor kecocokan tiap pasangan murid–tutor berdasarkan preferensi        |
| **Constraint Fulfillment** | Rata-rata persentase preferensi yang terpenuhi (5 aspek)                      |
| **Execution Time**       | Lama waktu yang dibutuhkan untuk menyelesaikan 1 run GA                        |
| **Deterministic**        | Apakah hasil GA selalu konsisten jika dijalankan 3× dengan input yang sama     |

---

## 🧪 Skenario Pengujian

| **Nama File**                         | **Deskripsi Skenario**                                                     |
|--------------------------------------|----------------------------------------------------------------------------|
| `scenario1_fixed.csv`                | Skenario 1 – Dataset ideal, lengkap 10 pasang                              |
| `scenario 2_5_fixed.csv`             | Skenario 2.1 – 5 pasang (tes skalabilitas kecil)                           |
| `scenario 2_10_fixed.csv`            | Skenario 2.2 – 10 pasang (tes skalabilitas sedang)                         |
| `scenario 2_25_fixed.csv`            | Skenario 2.3 – 25 pasang (tes skalabilitas besar)                          |
| `scenario3_conflict_heavy_fleksibel.csv` | Skenario 3 – Rebutan tutor populer, konflik preferensi tinggi             |

---

## 📈 Visualisasi & Analisis *(opsional)*
- 📉 Grafik performa terhadap jumlah data (menggunakan `matplotlib`)
- 🔗 Visualisasi matching dengan graf bipartit (menggunakan `networkx`)

---

## ✍️ Penulis
> **Wayan Raditya Putra**  
> Teknik Informatika – AI Engineering, ITS  
> Final Project – KKA 2025
