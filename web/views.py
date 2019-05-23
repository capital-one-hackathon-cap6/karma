import json
import random
import string
import pyrebase

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User

config = {
  "apiKey": "AIzaSyAfPQO0_5nmm0dOXxKBYU5TnTcEJHc2rq8",
  "authDomain": "karma-d09a3.firebaseapp.com",
  "databaseURL": "https://karma-d09a3.firebaseio.com",
  "storageBucket": "karma-d09a3.appspot.com"
}

firebase = pyrebase.initialize_app(config).database()

def get_keys(dir):
	ret = firebase.child(dir).shallow().get().val()
	return list(ret) if ret else []

def get_val(dir):
	return firebase.child(dir).get().val()

def index_view(request):
	data = {}
	data['requests'] = []
	reqs = get_keys('server_requests')
	for i, req in enumerate(reqs):
		data['requests'].append(dict(get_val('server_requests/%s' % req)))
	return render(request, 'web/index.html', data)