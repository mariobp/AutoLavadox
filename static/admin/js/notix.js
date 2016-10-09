var recive = true;

function Notix(){

}

Notix.prototype = {
	socket: null,
	django_id: null,
	event: null,
	callback: null,
	data: {},

	setup: function (session_id) {
		var self = this;
		$.ajax({
			'url': '/notificaciones/connections/',
			success: function (data) {
				self.socket = io(data);
				self.start(session_id);
			}
		});
	},

	start: function (session_id){
		this.django_id = session_id;
		this.socket.on('identify', function (message) {
			console.log(message);
			if (!message['ID']){
				this.login();
			}else{
				this.do_event();
			}
		}.bind(this));

		this.socket.on('success-login', function (message) {
			console.log("Ok");
			this.do_event();
		}.bind(this));

		this.socket.on('error-login', function (message) {
			console.log("Error");
		});

		this.socket.on('notix', function (message) {
			console.log(message);
			if (recive){
				var noti = notification(message.data.html);
				noti.onclick = function (){
					this.visit([message._id], function(){
						window.location = message.data.url;
					});
				}.bind(this);
			}
		}.bind(this));

		this.socket.on('visited', function (message) {
			console.log('visited', message);
			this.emit('messages', {
				'django_id': this.django_id ,
				 'usertype': 'WEB',
				 'webuser': username,
				 'type': type
			});
		}.bind(this));
		this.visit_path();
	},

	do_event: function (){
		if (this.event){
			this.socket.emit(this.event, this.data);
			this.event = null;
			this.data = {};
			if (this.callback){
				this.callback();
				this.callback = null;
			}
		}
	},

	emit: function (event, data, callback){
		this.event = event;
		this.data = data;
		console.log(event, "identify");
		this.socket.emit('identify', {"django_id": this.django_id, "usertype": "WEB"});
	},

	visit_path: function (){
		console.log("visit_path");
		this.emit('visited-path', {
			'django_id': this.django_id ,
			'usertype': 'WEB',
			'webuser': username,
			'path': window.location.pathname,
			'type': type
		});
	},

	visit: function (messages_id, callback){
		this.callback = callback;
		this.emit('visited', {
			'django_id': this.django_id ,
			'usertype': 'WEB',
			'webuser': username,
			'messages_id': messages_id,
			'type': type
		});
	},

	login: function(){
		this.socket.emit('login', {
			"username": "user1",
			"password": "123456",
			"usertype": "WEB",
			"django_id": this.django_id,
			"webuser": username
		});
	}

};

var notix = new Notix();
var notifications = [];

function notification(html) {
	var notification;
	var opt = {
		'icon': '/media/piscix_logo/notix.png'
	};
	if (!("Notification" in window)) {
		alert("This browser does not support desktop notification");
	}
	else if (Notification.permission === "granted") {
		notification = new Notification(html, opt);
		notifications.push(notification);
	} else if (Notification.permission !== 'denied') {
		Notification.requestPermission(function (permission) {
			if (permission === "granted") {
				notification = new Notification(html, opt);
				notifications.push(notification);
			}
		});
	}
	return notification;
}

function closeAll(){
	recive = false;
	for (notification in notifications) {
		notifications[notification].close();
	}
}
window.addEventListener("beforeunload", function (event) {
	closeAll();
});
