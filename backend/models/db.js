const { Pool } = require('pg');
require('dotenv').config();

// Configuración de la conexión
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

// Probar la conexión
pool.connect()
    .then(() => console.log('Connected to the PostgreSQL database'))
    .catch((err) => console.error('Error connecting to the database:', err));

module.exports = pool;
