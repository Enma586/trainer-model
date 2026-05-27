require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const sismosRoutes = require('./routes/sismosRoutes');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/sismos_db';

// Middlewares
app.use(cors());
app.use(express.json());

// Conexión a MongoDB
mongoose.connect(MONGO_URI)
    .then(() => console.log('Conectado exitosamente a MongoDB'))
    .catch(err => console.error('Error conectando a MongoDB:', err));

// Rutas base
app.use('/api/v1/sismos', sismosRoutes);

app.get('/', (req, res) => {
    res.json({ mensaje: "API Gateway de Sismos funcionando y conectado a BD 🚀" });
});

app.listen(PORT, () => {
    console.log(`Servidor Node corriendo en el puerto ${PORT}`);
});