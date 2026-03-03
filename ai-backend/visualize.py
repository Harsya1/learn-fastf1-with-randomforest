import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fastf1.plotting
import os

def plot_degradation(excel_file=os.path.join('data', 'data_telemetri_f1.xlsx'), output_image=os.path.join('plots', 'degradation_plot.png')):
    print(f"Membaca data dari {excel_file}...")
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"{excel_file} tidak ditemukan!")
        
    df = pd.read_excel(excel_file)
    
    # Memuat sesi untuk mendapatkan pemetaan warna kompon yang benar
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(2023, 'Bahrain', 'R')
    session.load(telemetry=False, weather=False, messages=False)
    
    # Setup tema F1 bawaan fastf1
    fastf1.plotting.setup_mpl(color_scheme='fastf1')
    
    plt.figure(figsize=(10, 6))
    
    for comp in df['Compound'].unique():
        subset = df[df['Compound'] == comp]
        # Menggunakan get_compound_color dengan menyertakan objek session
        color = fastf1.plotting.get_compound_color(comp, session=session)
        
        plt.scatter(subset['TyreLife'], subset['LapTime_s'], 
                    label=comp, color=color, alpha=0.8, s=60)
        
    plt.title('Kurva Degradasi Waktu vs Umur Ban (VER - Bahrain 2023)', fontsize=14)
    plt.xlabel('Umur Ban (Laps)')
    plt.ylabel('Waktu Lap (Detik)')
    plt.legend(title='Compound')
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    if not os.path.exists('plots'):
        os.makedirs('plots')
    plt.savefig(output_image, dpi=300)
    print(f"Visualisasi berhasil disimpan sebagai: {output_image}")

if __name__ == "__main__":
    plot_degradation()
