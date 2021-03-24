var express = require('express');
var app = express();

const port = 8000;
const mysql = require("mysql2");
  

app.get('/', function(req, res) {

const connection = mysql.createConnection({
  host: "mysql-db",
  user: process.env.DB_LOGIN,
  database: process.env.DB_NAME,
  password: process.env.DB_PWD"
});
connection.connect(function(err){
    if (err) {
    	res.send("Error" + err.message);
	}
    else{
      res.send('Connection successfull');
    }
 });


});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
});
