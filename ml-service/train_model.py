import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
import os

# Rutas de los archivos
DATA_PATH = "data/sismos.csv"
MODEL_DIR = "models"
MODEL_PATH = f"{MODEL_DIR}/random_forest.pkl"

def entrenar_modelo():
    print("1. Cargando dataset de sismos...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {DATA_PATH}. Asegúrate de ponerlo en la carpeta data/.")
        return

    # 2. Definir Features (Entrada) y Target (Salida)
    X = df[['latitud', 'longitud', 'profundidad_km']]
    y = df['magnitud']

    # 3. Dividir los datos (80% entrenamiento, 20% prueba)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("2. Entrenando el modelo Random Forest Regressor...")
    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    # 4. Evaluar el modelo
    predicciones = modelo_rf.predict(X_test)
    mse = mean_squared_error(y_test, predicciones)
    mae = mean_absolute_error(y_test, predicciones)
    
    print("\n--- RESULTADOS DE LA EVALUACIÓN ---")
    print(f"Error Cuadrático Medio (MSE): {mse:.4f}")
    print(f"Error Absoluto Medio (MAE): {mae:.4f}")

    # 5. Guardar el modelo entrenado
    print("\n3. Exportando el modelo...")
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        
    joblib.dump(modelo_rf, MODEL_PATH)
    print(f"¡Éxito! Modelo guardado en: {MODEL_PATH}")

if __name__ == "__main__":
    entrenar_modelo()