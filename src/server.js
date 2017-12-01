var fs = require('fs');
var http = require('http');
var express = require('express');


/*  This generates HTML that will display in browser listing all CSV files
 */
function getAllCSVs(){
	var files = fs.readdirSync('../sampleData');
	var dropdownModule = "";
	for(i = 0; i < files.length; i++){
		var option = "\n<li>" + files[i] + "</li>";
		dropdownModule += option;
	}
	return dropdownModule;
}

app = express();

app.use('/', express.static(__dirname + '/'));

/*  Frontend queries /csvload to get the CSV list
 */
app.get('/csvload', function(req, res){
  res.send(getAllCSVs());
  res.end();
});

var port = 80;
app.listen(port);
console.log("Server running on port " + port);
