Informe Técnico: Sismo Risk API
Este repositorio contiene el backend de un sistema predictivo de riesgos sísmicos para El Salvador. La solución emplea una arquitectura de microservicios contenerizada mediante Docker, integrando un motor de inferencia en Python y una API Gateway en Node.js para la gestión de datos y persistencia.

1. Arquitectura del Sistema
El ecosistema se basa en la orquestación de tres servicios principales:

API Gateway (Node.js/Express): Actúa como el único punto de entrada para el cliente. Se encarga del enrutamiento, validación de esquemas, gestión de políticas CORS y la interacción con la capa de persistencia.

Microservicio de Machine Learning (Python/FastAPI): Servicio especializado que ejecuta un modelo de regresión basado en el algoritmo Random Forest. Procesa las variables de entrada para estimar magnitudes sísmicas en tiempo real.

Capa de Persistencia (MongoDB): Base de datos NoSQL que almacena el registro histórico de cada predicción realizada, permitiendo el análisis posterior y la auditoría de datos.

2. Estructura de Directorios
Plaintext
sismo-backend/
├── docker-compose.yaml       # Configuración de orquestación de servicios
├── ml-service/               # Servicio de Inteligencia Artificial (Python)
│   ├── data/                 # Dataset de entrenamiento (sismos.csv)
│   ├── models/               # Binarios del modelo (.pkl)
│   ├── app.py                # Implementación de FastAPI
│   └── train_model.py        # Script de entrenamiento y generación del modelo
└── api-gateway/              # Gateway de Servicios (Node.js)
    ├── src/
    │   ├── controllers/      # Lógica de negocio y coordinación de servicios
    │   ├── models/           # Definición de esquemas de Mongoose
    │   └── routes/           # Definición de endpoints de la API
    └── server.js             # Punto de entrada del servidor Express
3. Requisitos del Sistema
Docker Engine y Docker Compose instalados.

Presencia del conjunto de datos sismos.csv en el directorio ml-service/data/.

4. Despliegue de la Infraestructura
El despliegue está automatizado para garantizar la portabilidad entre entornos de desarrollo y producción:

Acceder a la raíz del proyecto: cd sismo-backend/.

Ejecutar el proceso de construcción y levantamiento de contenedores:

Bash
docker compose up --build -d
Monitoreo de logs para verificar la inicialización de los servicios y la conexión a la base de datos:

Bash
docker compose logs -f
El servicio estará disponible para consumo en http://localhost:3000.

5. Especificación de la API
5.1 Predicción de Magnitud
Endpoint: POST /api/v1/sismos/predict

Descripción: Recibe coordenadas geográficas y profundidad, solicita la inferencia al microservicio de ML, clasifica el nivel de riesgo y persiste el resultado en MongoDB.

Cuerpo de la petición (JSON):

JSON
{
  "latitud": 13.18,
  "longitud": -89.41,
  "profundidad_km": 62.2
}
Respuesta exitosa (200 OK):

JSON
{
  "success": true,
  "data": {
    "magnitud_estimada": 4.5,
    "nivel_riesgo": "Medio",
    "parametros_usados": {
      "latitud": 13.18,
      "longitud": -89.41,
      "profundidad_km": 62.2
    }
  },
  "mensaje": "Predicción calculada y guardada en la base de datos."
}
5.2 Consulta de Historial
Endpoint: GET /api/v1/sismos/history

Descripción: Recupera los registros históricos de las predicciones almacenadas en la base de datos. Este endpoint está diseñado para alimentar componentes de visualización como mapas de calor o tablas de monitoreo.

Respuesta exitosa (200 OK): Devuelve un arreglo de objetos con el histórico completo de consultas, incluyendo sellos de tiempo y resultados de inferencia.
