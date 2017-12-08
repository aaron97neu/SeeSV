var fs = require("fs");
var http = require("http");
var express = require("express");
var path = require("path");
var chokidar = require("chokidar");
var mongoose = require("mongoose");
var passport = require("passport");
var flash = require("connect-flash");

var morgan = require("morgan");
var cookieParser = require("cookie-parser");
var bodyParser = require("body-parser");
var session = require("express-session");

var configDB = require("./config/database.js");

var port = process.env.PORT || 81; // Either the env var PORT or 80

//setup db
mongoose.connect(configDB.url);

// Passport
require('./config/passport')(passport)



//setup file watcher
var watcher = chokidar.watch(path.join(__dirname, '../sampleData'), {
  ignored: /(^|[\/\\])\../,
  persistent: true
});
var log = console.log.bind(console);

//run initial python code


//setup server static

app = express();
var serveDir = path.join(__dirname, 'csvs'); 
app.use(express.static(serveDir));

app.use(morgan('dev')); // log requests to stdout
app.use(cookieParser()); // read cookies
app.use(bodyParser()); // get info from html forms

app.set('view engine', 'ejs'); //use ejs for templating

//pasport setup
app.use(session({ secret: 'STAIRS!? NOOOOOOOOOOOOO!'}));
app.use(passport.initialize());
app.use(passport.session()); //persistent login
app.use(flash()); // use connect-flash

require('./app/routes.js')(app, passport); //load routes and pass into app and passport

//start listening
app.listen(port);
console.log('Server running on port ' + port);
//console.log('Serving all files in directory '+serveDir+'');

/*  This generates HTML that will display in browser listing all CSV files */
function getAllCSVs(){
	var files = fs.readdirSync('../sampleData');
	var dropdownModule = "";
	for(i = 0; i < files.length; i++){
		var option = "<button class=\"dropdown-item\" type=\"button\">"
			 + files[i] + "</button>\n"
		dropdownModule += option;
	}
	return dropdownModule;
}

/* Will create the dygraph and return javascript to be displayed on frontend*/
function returnDygraph(filename){
	console.log("Filename: " + filename);
}

/*  Frontend queries /csvload to get the CSV list*/
app.get('/csvload', function(req, res){
  res.send(getAllCSVs());
  res.end();
});

/*  Frontend queries /csvload to get the CSV list*/
app.get('/dygraphload', function(req, res){
  res.send(returnDygraph("a_file.csv"));
  res.end();
});

//setup event listeners
watcher
  .on('ready', () => log('Initial scan complete. Ready for changes'))
  .on('error', error => log(`Watcher error: ${error}`))
  .on('add', path => log(`File ${path} has been added`))
  .on('change', path => log(`File ${path} has been changed`))
  .on('unlink', path => log(`File ${path} has been removed`));

/*
// More possible events.
watcher
  .on('addDir', path => log(`Directory ${path} has been added`))
  .on('unlinkDir', path => log(`Directory ${path} has been removed`))
  .on('error', error => log(`Watcher error: ${error}`))
  .on('ready', () => log('Initial scan complete. Ready for changes'))
  .on('raw', (event, path, details) => {
    log('Raw event info:', event, path, details);
  });

// 'add', 'addDir' and 'change' events also receive stat() results as second
// argument when available: http://nodejs.org/api/fs.html#fs_class_fs_stats
watcher.on('change', (path, stats) => {
  if (stats) console.log(`File ${path} changed size to ${stats.size}`);
});*/
