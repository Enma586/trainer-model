import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import joblib
import os

# Rutas de los archivos locales
DATA_PATH = "data/sismos.csv"
MODEL_PATH = "models/random_forest.pkl"

def generar_graficas():
    print("Iniciando generación de gráficas...")

    # 1. Validar existencia de archivos
    if not os.path.exists(MODEL_PATH):
        print(f"Error: No se encontró el modelo en {MODEL_PATH}.")
        return
        
    if not os.path.exists(DATA_PATH):
        print(f"Error: No se encontró el dataset en {DATA_PATH}.")
        return

    # 2. Cargar modelo y datos históricos
    modelo_rf = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)
    
    # Extraer los nombres de las variables de entrada
    X = df[['latitud', 'longitud', 'profundidad_km']]
    variables = X.columns

    # ==========================================
    # GRÁFICO 1: Importancia de Variables
    # ==========================================
    print("Generando gráfico de importancia de variables...")
    importancias = modelo_rf.feature_importances_

    plt.figure(figsize=(8, 5))
    colores = ['#4CAF50', '#2196F3', '#FF9800']
    plt.bar(variables, importancias, color=colores)
    
    plt.title('Importancia de Variables (Random Forest)')
    plt.ylabel('Nivel de Importancia')
    plt.xlabel('Características')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Guardar imagen y limpiar lienzo
    plt.savefig('importancia_variables.png', bbox_inches='tight', dpi=300)
    plt.clf() 

    # ==========================================
    # GRÁFICO 2: Árbol de Decisión
    # ==========================================
    print("Generando gráfico del árbol de decisión...")
    
    # Extraer el primer árbol (índice 0) del ensamble Random Forest
    arbol_ejemplo = modelo_rf.estimators_[0]

    # Ajustes de lienzo y fuente para evitar solapamiento de nodos
    plt.figure(figsize=(25, 12)) 
    
    plot_tree(arbol_ejemplo, 
              feature_names=variables, 
              filled=True, 
              rounded=True, 
              max_depth=3, 
              fontsize=8,        # Fuente reducida para mejor ajuste
              precision=3,       # Limitado a 3 decimales
              proportion=False)
    
    plt.title('Estructura Interna: Árbol de Decisión #1') 
    
    # Guardar imagen en alta resolución
    plt.savefig('arbol_decision.png', dpi=300, bbox_inches='tight')
    
    print("Proceso finalizado. Gráficas guardadas en el directorio actual.")

if __name__ == "__main__":
    generar_graficas()