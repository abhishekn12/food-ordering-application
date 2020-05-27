var express = require('express');
var mysql = require('mysql');
var app = express();

var connection = mysql.createConnection({
	//properties..
	host: 'localhost',
	user: 'root',
	password: '',
	database: 'menu'
});

connection.connect(function (err){
	if(!err){
		console.log("Connection established");
		connection.query("SELECT * FROM menu", function(err,result,fields){
			if(err) throw err;
			Object.keys(result).forEach(function(key) {
				var row = result[key];
				console.log(row.name)
			});
		});
	}
	else console.log("Connection Failed");
});


app.listen(1337);
