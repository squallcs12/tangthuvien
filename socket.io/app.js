var app = require('express')();
var server = require('http').createServer(app);
var io = require('socket.io').listen(server);
var sys = require('sys');
var exec = require('child_process').exec;

server.listen(8001);

app.get('/', function(req, res) {
	res.sendfile(__dirname + '/index.html');
});
(function(){
	var running = false;
	generate_book_prc = function(data) {
		if(running){
			return;
		}
		running = true;
		book_id = data['book_id'];
		exec("cd ..; ./env/bin/python manage.py generate_prc -j 1 -b " + book_id, function(error, stdout, stderr) {
			var attachment = JSON.parse(stdout);
			io.sockets.emit('generate_book_prc_' + book_id, {
				attachment: attachment
			});
			running = false;
		});
	};
})();
io.sockets.on('connection', function(socket) {
	socket.on('generate_book_prc', generate_book_prc);
});