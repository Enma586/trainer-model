# 1. Imagen base de Python ligera
FROM python:3.11-slim

# 2. Directorio de trabajo en el contenedor
WORKDIR /app

# 3. Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar todo el código fuente y la data
COPY . .

# 5. Entrenar el modelo automáticamente durante la construcción


# 6. Exponer el puerto de FastAPI
EXPOSE 8000

# 7. Comando para arrancar el servidor
CMD sh -c "python train_model.py && python visualizar_modelo.py && uvicorn app:app --host 0.0.0.0 --port 8000"