import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib

# Import fungsi pembantu dari skrip get_data
from get_data import extract_telemetry_data

def train_tyre_degradation_model():
    print("Memulai ekstraksi dan pra-pemrosesan data...")
    # Kita menggunakan pembalap default (VER) untuk percobaan
    df = extract_telemetry_data()
    
    print("Mempersiapkan fitur untuk Machine Learning...")
    # 1. Konversi Tipe Data Categorical
    # Kolom 'Compound' berisi teks 'SOFT', 'MEDIUM', 'HARD'. 
    # Karena Random Forest butuh format numerik, kita ubah teks tersebut 
    # menggunakan metod One-Hot Encoding (OHE).
    df = pd.get_dummies(df, columns=['Compound'], drop_first=False)
    
    # 2. Definisikan Independen Variable (X) dan Dependen Variable (Target / y)
    # Tujuan utama SPK ini adalah menaksir (memprediksi) LapTime (Y)
    # dari degradasi berdasarkan umur ban, cuaca, dan tingkat komponnya (X).
    feature_cols = ['TyreLife', 'AirTemp', 'TrackTemp'] + [c for c in df.columns if c.startswith('Compound_')]
    X = df[feature_cols]
    y = df['LapTime_s']
    
    # 3. Pembagian Data Pelatihan (80%) dan Data Tes (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Implementasi Model Algoritma Utama (Sesuai Aturan: RandomForestRegressor)
    print("Melatih model RandomForestRegressor...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # 5. Evaluasi Metrik Prediksi
    y_pred = rf_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2_score = rf_model.score(X_test, y_test)
    
    print("\n================ EVALUASI MODEL ================")
    print(f"Root Mean Squared Error (RMSE): {rmse:.3f} detik")
    print(f"Mean Absolute Error (MAE)     : {mae:.3f} detik")
    print(f"Akurasi Model R² Score        : {r2_score:.3f}")
    print("================================================\n")
    
    # 6. Ekspor Model Agar Siap Digunakan Oleh API (Tahap Lanjutan/Fase Berikutnya)
    model_filename = "rf_tyre_model.joblib"
    joblib.dump(rf_model, model_filename)
    print(f"Berhasil! Model diekspor ke format joblib: {model_filename}")

if __name__ == "__main__":
    train_tyre_degradation_model()
