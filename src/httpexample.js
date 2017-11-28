var http = require("http");
var numVisitors = 0;

http.createServer(function (request, response) {
   // Send the HTTP header 
   // HTTP Status: 200 : OK
   // Content Type: text/plain
   response.writeHead(200, {'Content-Type': 'text/plain'});
   numVisitors = numVisitors + 1;
   console.log('Visitor number '+String(numVisitors)+' has arrived');
   //console.log('The host came from: '+String(request.headers));
   // Send the response body as "Hello World"
   
   response.end('Hello World\nYou are vistor number ' + String(numVisitors));
}).listen(81);

// Console will print the message
console.log('Server running at http://127.0.0.1:81/');
