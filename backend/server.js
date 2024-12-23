const express = require('express');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Configuración de la base de datos
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
  ssl: {
    rejectUnauthorized: false, // Esto es importante para conexiones externas con Render
  },
});

// Middleware para parsear JSON
app.use(express.json());

// Ruta de prueba
app.get('/', (req, res) => {
  res.send('API funcionando correctamente');
});

// Endpoint para obtener datos de una tabla específica (ejemplo)
app.get('/api/items', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM items'); // Cambia "items" por el nombre de tu tabla
    res.json(result.rows);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error al obtener los datos');
  }
});

// Endpoint para insertar datos en una tabla específica (ejemplo)
app.post('/api/items', async (req, res) => {
  const { name, description } = req.body; // Ajusta según las columnas de tu tabla
  try {
    const result = await pool.query(
      'INSERT INTO items (name, description) VALUES ($1, $2) RETURNING *',
      [name, description]
    );
    res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error al insertar los datos');
  }
});

// Inicializar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
