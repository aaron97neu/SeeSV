var http = require("http");
var express = require("express");
var path = require("path");
var chokidar = require("chokidar");

//setup file watcher
var watcher = chokidar.watch(path.join(__dirname, 'csvs'), {
  ignored: /(^|[\/\\])\../,
  persistent: true
});
var log = console.log.bind(console);
var ready = 0;
//run initial python code


//setup server
app = express();
var serveDir = path.join(__dirname, 'public'); 
app.use(express.static(serveDir));
var port = 82; // Change this

//start listening
app.listen(port);
console.log('Server running on port ' + port);
console.log('Serving all files in directory '+serveDir+'');

//setup event listeners
watcher
  .on('ready', () => {
    log('Initial scan complete. Ready for changes');
    ready = 1;
  })
  .on('error', error => log(`Watcher error: ${error}`))
  .on('add', path => log(`File ${path} has been added`))
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
