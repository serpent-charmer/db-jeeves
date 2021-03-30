const express = require('express');
const path = require('path');
const { Client } = require('pg');

const port = 8000;
const mysql = require("mysql2");




express()
    .use(express.static(path.join(__dirname, 'public')))
    .set('views', path.join(__dirname, 'views'))
    .set('view engine', 'ejs')
    .get('/', (req, res) => res.render('pages/main'))
    .get('/test_db', function (req, res_exp) {

        const client = new Client({
            user: process.env.DB_LOGIN,
            host: 'pgsql-db',
            database: process.env.DB_NAME,
            password: process.env.DB_PWD,
          })
        client.connect()
        client.query('SELECT $1::text as message', ['Hello world!'], (err, res) => {
            client.end()
            res_exp.send(err ? err.stack : res.rows[0].message)
        })

        // const connection = mysql.createConnection({
        //     host: "mysql-db",
        //     user: process.env.DB_LOGIN,
        //     database: process.env.DB_NAME,
        //     password: process.env.DB_PWD
        // });

        // connection.connect(function (err) {
        //     if (err) {
        //         res.send("Error" + err.message);
        //     }
        //     else {
        //         res.send('Connection successfull');
        //     }
        // });
    })

    .listen(port, () => {
        console.log(`Example app listening at http://localhost:${port}`)
    });
