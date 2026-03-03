import fastf1
import pandas as pd
import os

def explore_millisecond_telemetry():
    print("Memuat data sesi (mengaktifkan telemetri penuh)...")
    # Setup cache
    fastf1.Cache.enable_cache('cache')
    
    # Load session dengan telemetry=True
    session = fastf1.get_session(2023, 'Bahrain', 'R')
    session.load(telemetry=True, weather=False, messages=False)
    
    # Ambil lap tercepat dari Max Verstappen
    fastest_ver = session.laps.pick_driver('VER').pick_fastest()
    print(f"\nLap Tercepat VER: {fastest_ver['LapTime']}")
    
    # Ambil data telemetri milidetik (Car Telemetry) untuk lap tercepat tersebut
    telemetry_data = fastest_ver.telemetry
    
    # Tampilkan info
    print("\n=== Kolom Data Telemetri Milidetik ===")
    print(telemetry_data.columns.tolist())
    
    print(f"\nTotal Titik Rekaman Data (Hanya untuk 1 putaran ini!): {len(telemetry_data)} baris")
    
    # Tampilkan beberapa sampel data yang relevan
    print("\n=== Cuplikan Data (Speed, Throttle, Brake, RPM, X, Y) ===")
    sample_cols = ['Time', 'Speed', 'Throttle', 'Brake', 'RPM', 'X', 'Y', 'Z']
    print(telemetry_data[sample_cols].head(10))

    # D. Konversi kolom Time (timedelta) ke float detik murni agar lebih readable
    # Contoh: '0 days 00:00:00.062000' -> 0.062
    telemetry_export = telemetry_data.copy()
    telemetry_export['Time_s'] = telemetry_export['Time'].dt.total_seconds()
    
    # Tampilkan preview dengan format Time yang sudah dikonversi
    print("\n=== Cuplikan Data dengan Time dalam Satuan Detik (float) ===")
    print(telemetry_export[['Time_s', 'Speed', 'Throttle', 'Brake', 'RPM', 'X', 'Y']].head(10).to_string())

    # Ekspor ke Excel di folder data/
    if not os.path.exists('data'):
        os.makedirs('data')

    # Buang kolom Time asli (timedelta) agar Excel tidak error, gunakan Time_s
    cols_to_export = [c for c in telemetry_export.columns if c != 'Time'] 
    export_path = os.path.join('data', 'telemetry_ver_fastest.xlsx')
    print(f"\nMengekspor data {len(telemetry_export)} baris ke {export_path}...")
    telemetry_export[cols_to_export].to_excel(export_path, index=False)
    print("Ekspor selesai!")

if __name__ == "__main__":
    explore_millisecond_telemetry()
