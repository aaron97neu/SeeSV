var http = require("http");
var express = require("express");
var path = require("path");

app = express();

var serveDir = path.join(__dirname, 'public'); 

app.use(express.static(serveDir));

var port = 81; // Change this

app.listen(port);
console.log('Server running on port ' + port);
console.log('Serving all files in directory '+serveDir+'');
