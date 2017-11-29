var http = require("http");
var express = require("express");
app = express();
app.use('/', express.static(__dirname + '/'));
//app.use('/csvload', express.static(__dirname + '/csv-dropdown.js'));
//app.use('/select.html', express.static(__dirname + '/select.html'));

var port = 80; // Change this

app.listen(port);
console.log('Server running on port ' + port);
