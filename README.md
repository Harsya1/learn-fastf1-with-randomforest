# Sistem Pendukung Keputusan F1 (Fase 1: AI & Machine Learning)

Repositori ini berisi kode dan model untuk memprediksi degradasi ban mobil Formula 1. Model Machine Learning ini dibangun sebagai inti dari Sistem Pendukung Keputusan (SPK) strategi balap.

## Fitur Utama
- **Ekstraksi Data:** Menggunakan pustaka `fastf1` dengan mekanisme sistem cache agar responsif.
- **Pra-pemrosesan Data:** Transformasi waktu ke format numerik murni dan filter kondisi balapan (Safety Car, dll).
- **Machine Learning:** Menggunakan `RandomForestRegressor` dari `scikit-learn` untuk memprediksi kurva degradasi.

## Instruksi Penggunaan (Lokal)
1. Buat virtual environment: `python -m venv venv`
2. Aktifkan virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies terkait (pastikan terinstall `fastf1`, `pandas`, `numpy`, `scikit-learn`).

*Proyek ini diformulasikan untuk keperluan Seminar Proposal/Skripsi.*
