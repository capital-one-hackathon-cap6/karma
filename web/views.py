import json
from jsonschema import validate, ValidationError
import random
import requests
import string
import pyrebase
from twilio.rest import Client

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Twilio
account_sid = 'AC2b1dac17ce21e51df47483a5e541efb3'
auth_token = '8c3adea94a99b9b09aaf7e4dfc9fd8ed'
twilio_num = '+18136941083'

# Nessie
nessie_key = 'b09e86c3728a8ecd3067e84cadbae461'

config = {
    "apiKey": "AIzaSyAfPQO0_5nmm0dOXxKBYU5TnTcEJHc2rq8",
    "authDomain": "karma-d09a3.firebaseapp.com",
    "databaseURL": "https://karma-d09a3.firebaseio.com",
    "storageBucket": "karma-d09a3.appspot.com"
}

firebase = pyrebase.initialize_app(config).database()


def push_data(card_id, lat, lon, time):
    export_data = {
        'card_id': card_id,
        'location': {
            'lat': lat,
            'long': lon
        },
        'time': time,
        'status': 'Locked'
    }
    firebase.child("server_requests").child(card_id).update(export_data)


def get_keys(dir):
    ret = firebase.child(dir).shallow().get().val()
    return list(ret) if ret else []


def get_val(dir):
    return firebase.child(dir).get().val()


def valid_json(body):
    schema = {
        "type": "object",
        "properties": {
                "location": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"}
                },
            "time": {"type": "string"},
            "card_id": {"type": "string"},
            "status": {"type": "string"}
        }
    }

    try:
        validate(instance=body, schema=schema)
    except ValidationError:
        return False

    return True


def get_phone_number_or_invalid(card_id):
    response = requests.get(
        f'http://api.reimaginebanking.com/enterprise/customers/{card_id}?{nessie_key}')  # This API doesn't work how we need it too

    if response.status_code == 200:
        # return response['phone_num']
        return '+18137898024'
    else:
        # We don't have access to an API that gives customer information from a CC number
        # return 'invalid'
        return '+18137898024'


def lock_card(card_id):
    requests.post(
        f'http://api.reimaginebanking.com/enterprise/accounts/{card_id}?{nessie_key}')  # Fake API call


def send_alert(card_id, lat, lon, time, phone_num):
    last_four = card_id[-4:]

    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=f'Alert:\nYour Capital one card, ending in {last_four}, was reported as lost at {time} and has been automatically locked. Follow this link to view the location. Reply CANCEL to cancel your card.\nhttps://www.google.com/maps/@{lat},{lon},19z',
            from_=twilio_num,
            status_callback=HttpResponseRedirect(reverse('web:alert_callback')),
            to=phone_num
        )
    print("MSG SENT")


def index_view(request):
    data = {}
    data['requests'] = []
    reqs = get_keys('server_requests')
    for i, req in enumerate(reqs):
        data['requests'].append(dict(get_val('server_requests/%s' % req)))
    return render(request, 'web/index.html', data)


@csrf_exempt
def receive_alert(request):
    if request.method == 'POST':
        print('received request')
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if not valid_json(body):
            return HttpResponse(status=400)

        card_id = body['card_id']
        phone_num = get_phone_number_or_invalid(card_id)
        if phone_num == 'invalid':
            return HttpResponse(status=400)

        lock_card(card_id)

        lat = body['location']['lat']
        lon = body['location']['lon']
        time = body['time']

        push_data(card_id, lat, lon, time)
        send_alert(card_id, lat, lon, time, phone_num)

        return HttpResponse(status=200)


@csrf_exempt
def alert_callback(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body['MessageStatus'])
