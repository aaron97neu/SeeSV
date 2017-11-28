var http = require("http");
var express = require("express");
app = express();
app.use('/', express.static(__dirname + '/'));

var port = 80; // Change this

app.listen(port);
console.log('Server running on port ' + port);
