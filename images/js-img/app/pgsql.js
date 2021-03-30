const { Client } = require('pg');
const client = new Client({
    user: process.env.DB_LOGIN,
    host: 'pgsql-db',
    database: process.env.DB_NAME,
    password: process.env.DB_PWD,
  });
client.connect();
client.query('SELECT $1::text as message', ['Hello world!'], (err, res) => {
    client.end();
    res_exp.send(err ? err.stack : res.rows[0].message);
})