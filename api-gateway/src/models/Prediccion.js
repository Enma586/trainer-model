const mongoose = require('mongoose');

const prediccionSchema = new mongoose.Schema({
    latitud: { type: Number, required: true },
    longitud: { type: Number, required: true },
    profundidad_km: { type: Number, required: true },
    magnitud_estimada: { type: Number, required: true },
    nivel_riesgo: { type: String, required: true },
    fecha_consulta: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Prediccion', prediccionSchema);