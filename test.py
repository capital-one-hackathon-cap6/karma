import pyrebase

config = {
  "apiKey": "AIzaSyAfPQO0_5nmm0dOXxKBYU5TnTcEJHc2rq8",
  "authDomain": "karma-d09a3.firebaseapp.com",
  "databaseURL": "https://karma-d09a3.firebaseio.com",
  "storageBucket": "karma-d09a3.appspot.com"
}

firebase = pyrebase.initialize_app(config).database()

def push_data(card_id, location, time):
	export_data = {
		'card_id': card_id,
		'location': location,
		'time': time
	}
	firebase.child("server_requests").child(card_id).update(export_data)

push_data('12345678', '(123.4, 1531.3)', 'January 2nd')