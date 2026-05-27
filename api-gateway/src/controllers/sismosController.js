const axios = require('axios');
const Prediccion = require('../models/Prediccion'); // Importamos el modelo

const PYTHON_URL = process.env.PYTHON_SERVICE_URL || 'http://localhost:8000';

const predictMagnitude = async (req, res) => {
    try {
        const { latitud, longitud, profundidad_km } = req.body;

        if (!latitud || !longitud || !profundidad_km) {
            return res.status(400).json({ error: "Faltan parámetros." });
        }

        // 1. Pedir la predicción a Python
        const pythonResponse = await axios.post(`${PYTHON_URL}/predecir`, {
            latitud: parseFloat(latitud),
            longitud: parseFloat(longitud),
            profundidad_km: parseFloat(profundidad_km)
        });

        const prediccionData = pythonResponse.data;

        // 2. Guardar en MongoDB
        const nuevaPrediccion = new Prediccion({
            latitud,
            longitud,
            profundidad_km,
            magnitud_estimada: prediccionData.magnitud_estimada,
            nivel_riesgo: prediccionData.nivel_riesgo
        });
        await nuevaPrediccion.save();

        // 3. Responder al frontend
        return res.status(200).json({
            success: true,
            data: prediccionData,
            mensaje: "Predicción calculada y guardada en la base de datos."
        });

    } catch (error) {
        console.error("Error en el servidor:", error.message);
        return res.status(500).json({ success: false, error: "Error procesando la solicitud." });
    }
};
const getHistory = async (req, res) => {
    try {
        // Obtenemos las últimas 50 predicciones guardadas
        const historial = await Prediccion.find().sort({ fecha_consulta: -1 }).limit(50);
        
        return res.status(200).json({
            success: true,
            count: historial.length,
            data: historial
        });
    } catch (error) {
        console.error("Error obteniendo historial:", error.message);
        return res.status(500).json({ success: false, error: "No se pudo obtener el historial." });
    }
};

module.exports = { predictMagnitude, getHistory };