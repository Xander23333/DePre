let mysql = require('mysql');
let express = require('express');

console.log("hello world");

var connection = mysql.createConnection({
    host: '106.14.206.16',
    user: 'pepe',
    password: 'qwertyuiop',
    database: 'pepeGame'
});
connection.connect();
let app = express();

app.get('/', function (req, res) {

    connection.query('SELECT * FROM result', function (error, results, fields) {
        if (error) throw error;
        console.log('The solution is: ', results);
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
        res.header("X-Powered-By", ' 3.2.1')
        res.header("Content-Type", "application/json;charset=utf-8");
        res.send(results[results.length - 1]);
    });
});

let server = app.listen(3000, function () {
    let host = server.address().address;
    let port = server.address().port;
});
