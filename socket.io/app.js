var app = require('express')();
var server = require('http').createServer(app);
var io = require('socket.io').listen(server);
var sys = require('sys');
var exec = require('child_process').exec;

server.listen(1234);

app.get('/', function(req, res) {
	res.sendfile(__dirname + '/index.html');
});

io.sockets.on('connection', function(socket) {
	socket.on('generate_book_prc', function(data) {
		console.log(socket);
		book_id = data['book_id'];
		exec("cd ..; ./env/bin/python manage.py generate_prc -j 1 -b " + book_id, function(error, stdout, stderr) {
			var attachment = JSON.parse(stdout);
			io.sockets.emit('generate_book_prc_' + book_id, {
				attachment: attachment
			});
		});
	});
});