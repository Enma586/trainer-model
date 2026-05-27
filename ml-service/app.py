from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="API Predictiva de Sismos - UNAB")

# Ruta donde train_model.py guardó el cerebro
MODEL_PATH = "models/random_forest.pkl"
modelo_rf = None

# Estructura de datos que esperamos de Node.js
class DatosSismo(BaseModel):
    latitud: float
    longitud: float
    profundidad_km: float

# Evento de inicio: Cargar el modelo a la RAM
@app.on_event("startup")
def cargar_modelo():
    global modelo_rf
    if os.path.exists(MODEL_PATH):
        modelo_rf = joblib.load(MODEL_PATH)
        print("Modelo Random Forest cargado exitosamente.")
    else:
        print(f"ADVERTENCIA: No se encontró el modelo en {MODEL_PATH}.")

# Endpoint principal de predicción
@app.post("/predecir")
def predecir_riesgo(datos: DatosSismo):
    if modelo_rf is None:
        raise HTTPException(status_code=503, detail="El modelo no está entrenado o disponible.")
    
    try:
        # Formatear datos para el modelo
        X_nuevo = [[datos.latitud, datos.longitud, datos.profundidad_km]]
        
        # Realizar predicción
        prediccion_magnitud = modelo_rf.predict(X_nuevo)[0]
        
        # Lógica de semáforo de riesgo
        nivel_riesgo = "Bajo"
        if prediccion_magnitud >= 5.0:
            nivel_riesgo = "Alto"
        elif prediccion_magnitud >= 4.5:
            nivel_riesgo = "Medio"

        return {
            "magnitud_estimada": round(prediccion_magnitud, 2),
            "nivel_riesgo": nivel_riesgo,
            "parametros_usados": datos.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))