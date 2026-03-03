import fastf1
import pandas as pd

# 1. Setup Cache (Sangat penting agar tidak download ulang data berulang kali)
# Pastikan folder 'cache' ada di direktori yang sama
import os
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache') 

# 2. Load Session (Contoh: Musim 2023, Grand Prix Bahrain, Sesi 'R' atau Race)
# Bahrain dipilih karena karakteristik sirkuitnya yang sangat menguras ban (high degradation)
print("Loading data balapan...")
session = fastf1.get_session(2023, 'Bahrain', 'R')
session.load()

# 3. Ambil data Laps khusus untuk Max Verstappen ('VER')
print("\nMengambil data lap untuk VER...")
laps_ver = session.laps.pick_drivers('VER')

# 4. Filter kolom yang relevan untuk analisis degradasi ban
# LapNumber: Lap ke-berapa
# LapTime: Waktu tempuh lap tersebut
# Compound: Jenis ban (SOFT, MEDIUM, HARD)
# TyreLife: Umur ban (sudah dipakai berapa lap)
# TrackStatus: Status lintasan (1 = Normal, 4 = Safety Car, dll. Penting difilter nanti agar anomali data terbuang)
df_tyre_data = laps_ver[['LapNumber', 'LapTime', 'Compound', 'TyreLife', 'TrackStatus']]

# 5. Tampilkan 10 baris pertama
print("\n=== Data Telemetri Ban ===")
print(df_tyre_data.head(10))

# Opsional: Tampilkan info tipe data
print("\n=== Info Dataframe ===")
print(df_tyre_data.info())