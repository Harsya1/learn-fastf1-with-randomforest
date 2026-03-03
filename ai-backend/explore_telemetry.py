import fastf1
import fastf1.plotting
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

    # ================= VISUALISASI TELEMETRI ================= #
    print("\nMembuat visualisasi grafik telemetri milidetik...")
    
    # Siapkan tema FastF1
    fastf1.plotting.setup_mpl(color_scheme='fastf1')
    
    t = telemetry_export['Time_s']  # Waktu dalam detik (sumbu X)

    fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)
    fig.suptitle(
        f"Telemetri Milidetik Max Verstappen\nBahrain Grand Prix 2023 – Lap Tercepat ({fastest_ver['LapTime']})",
        fontsize=14, fontweight='bold'
    )

    # Panel 1: Kecepatan (Speed)
    axes[0].plot(t, telemetry_export['Speed'], color='#E8002D', linewidth=1.2)
    axes[0].set_ylabel('Kecepatan (km/h)')
    axes[0].set_ylim(0, 360)
    axes[0].grid(alpha=0.3)
    axes[0].set_title('Speed')

    # Panel 2: Injakan Gas (Throttle %)
    axes[1].plot(t, telemetry_export['Throttle'], color='#00D2BE', linewidth=1.2)
    axes[1].set_ylabel('Throttle (%)')
    axes[1].set_ylim(-5, 110)
    axes[1].grid(alpha=0.3)
    axes[1].set_title('Throttle')

    # Panel 3: Status Rem (Brake True/False)
    axes[2].fill_between(t, telemetry_export['Brake'].astype(int),
                         color='#FF8700', alpha=0.8, linewidth=0)
    axes[2].set_ylabel('Rem Aktif')
    axes[2].set_ylim(-0.1, 1.5)
    axes[2].set_yticks([0, 1])
    axes[2].set_yticklabels(['Off', 'On'])
    axes[2].grid(alpha=0.3)
    axes[2].set_title('Brake')

    axes[2].set_xlabel('Waktu dalam Lap (detik)')

    plt.tight_layout()

    # Simpan sebagai JPG di folder plots/
    if not os.path.exists('plots'):
        os.makedirs('plots')
    jpg_path = os.path.join('plots', 'telemetry_ver_fastest.jpg')
    plt.savefig(jpg_path, dpi=200, format='jpeg', bbox_inches='tight')
    print(f"Visualisasi berhasil disimpan: {jpg_path}")

if __name__ == "__main__":
    explore_millisecond_telemetry()
