const express = require('express');
const path = require('path');

const port = process.env.DEFAULT_PORT;




express()
    .use(express.static(path.join(__dirname, 'public')))
    .set('views', path.join(__dirname, 'views'))
    .set('view engine', 'ejs')
    .get('/', (req, res) => res.render('pages/main'))
    .get('/test_db', function (req, res) {

        
    })
    .listen(port, () => {
        console.log(`Example app listening at http://localhost:${port}`)
    });
