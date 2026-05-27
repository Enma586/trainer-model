const express = require('express');
const router = express.Router();
const { predictMagnitude, getHistory} = require('../controllers/sismosController');

// El frontend hará un POST a: http://localhost:3000/api/v1/sismos/predict
router.post('/predict', predictMagnitude);
// GET para obtener historial (para el Mapa de Calor)
router.get('/history', getHistory);

module.exports = router;