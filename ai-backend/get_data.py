import fastf1
import pandas as pd
import os

def extract_telemetry_data(year=2023, grand_prix='Bahrain', session_type='R', driver='VER'):
    """
    Mengekstraksi dan melakukan pra-pemrosesan data telemetri F1.
    Mengembalikan DataFrame pandas yang bersih dan siap untuk Machine Learning.
    """
    # 1. Setup Cache (Wajib diaktifkan di awal skrip)
    if not os.path.exists('cache'):
        os.makedirs('cache')
    fastf1.Cache.enable_cache('cache') 

    # 2. Mengambil Sesi
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load(telemetry=False, weather=True, messages=False)

    # 3. Ekstrak data lap untuk pembalap spesifik
    # Menggunakan pick_drivers() untuk menghindari FutureWarning
    laps_driver = session.laps.pick_drivers(driver)

    # 4. Mendapatkan data cuaca
    weather_data = laps_driver.get_weather_data()

    # Reset index agar penggabungan tidak kacau
    laps_driver.reset_index(drop=True, inplace=True)
    weather_data.reset_index(drop=True, inplace=True)
    
    # Gabungkan data lap dan cuaca
    df_tyre_data = pd.concat([laps_driver, weather_data], axis=1)

    # Pilih kolom yang relevan
    cols = ['LapNumber', 'LapTime', 'Compound', 'TyreLife', 'TrackStatus', 'AirTemp', 'TrackTemp', 'PitInTime', 'PitOutTime']
    df_tyre_data = df_tyre_data[[c for c in cols if c in df_tyre_data.columns]].copy()

    # ================= PRA-PEMROSESAN (PREPROCESSING) ================= #

    # A. Buang Anomali: Lap Out/In (Pit Laps)
    if 'PitInTime' in df_tyre_data.columns and 'PitOutTime' in df_tyre_data.columns:
        df_tyre_data = df_tyre_data[pd.isnull(df_tyre_data['PitOutTime']) & pd.isnull(df_tyre_data['PitInTime'])]
        df_tyre_data = df_tyre_data.drop(columns=['PitInTime', 'PitOutTime'])

    # B. Buang Anomali: Safety Car & Virtual Safety Car (Status lintasan selain 1 atau 2)
    # 1=Clear, 2=Yellow. 4=SC, 5=VSC dll.
    if 'TrackStatus' in df_tyre_data.columns:
        df_tyre_data = df_tyre_data[~df_tyre_data['TrackStatus'].astype(str).str.contains('4|5|6|7', regex=True)]

    # C. Atasi Missing Values LapTime
    df_tyre_data = df_tyre_data.dropna(subset=['LapTime', 'Compound', 'AirTemp', 'TrackTemp'])

    # D. Konversi Waktu Tempuh: Menjadi format numerik detik murni (float)
    df_tyre_data['LapTime_s'] = df_tyre_data['LapTime'].dt.total_seconds()
    
    # Buang kolom aslinya agar struktur DataFrame ramping
    df_tyre_data = df_tyre_data.drop(columns=['LapTime', 'TrackStatus', 'LapNumber'])

    return df_tyre_data

if __name__ == "__main__":
    df = extract_telemetry_data()
    print("\n=== Data Telemetri Ban Sesudah Di-Filter ===")
    print(df.head(10))
    print("\n=== Info Dataframe ===")
    print(df.info())
