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
var spawn = require("child_process").spawn;

//constants
var port = process.env.PORT || 80; // Either the env var PORT or 80
var ehabd_path = path.join(__dirname, 'ehabd_scripts/ehabdReduction.py');

//setup db
mongoose.connect(configDB.url);

// Passport
require('./config/passport')(passport)

//setup file watcher
var watcher = chokidar.watch(path.join(__dirname, 'csvs'), {
  ignored: /(^|[\/\\])\../,
  persistent: true
});
var log = console.log.bind(console);
var ready = 0;
//run initial python code


//setup server static

app = express();

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
	var files = fs.readdirSync('csvs');
	var dropdownModule = "";
	for(i = 0; i < files.length; i++){
		var option = "\n<li>" + files[i] + "</li>";
		dropdownModule += option;
	}
	return dropdownModule;
}

/*  Frontend queries /csvload to get the CSV list*/
app.get('/csvload', function(req, res){
  res.send(getAllCSVs());
  res.end();
});

//setup event listeners
watcher
  .on('ready', () => {
    log('Initial scan complete. Ready for changes');
    ready = 1;
  })
  .on('error', error => log(`Watcher error: ${error}`))
  .on('add', pathToFile => {
    log(`File ${pathToFile} has been added`);
    console.log('Running '+ehabd_path+' '+pathToFile);
    var ehabd = spawn('python3',[ehabd_path, pathToFile]);
    ehabd.stdout.on('data', function (data){
      if(data.toString().trim() === 'done'){
	console.log("Finished running ehabdReduction on "+path);
      }
    });
    
  })
  .on('change', path => log(`File ${path} has been changed`))
  .on('unlink', path => log(`File ${path} has been removed`));


/*
// Chokidar more possible events.
watcher
  .on('addDir', path => log(`Directory ${path} has been added`))
  .on('unlinkDir', path => log(`Directory ${path} has been removed`))
  .on('raw', (event, path, details) => {
    log('Raw event info:', event, path, details);
  });

// 'add', 'addDir' and 'change' events also receive stat() results as second
// argument when available: http://nodejs.org/api/fs.html#fs_class_fs_stats
watcher.on('change', (path, stats) => {
  if (stats) console.log(`File ${path} changed size to ${stats.size}`);
});*/
