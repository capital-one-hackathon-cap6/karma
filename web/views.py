import json
import random
import string
import io
import os

import requests
import base64
import datetime
import geocoder

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User

from luhn import *


'''
Given the string returned from the OCR algorithm, scrape for the bank number
'''
def find_credit_num(s):
    digits = [str(a) for a in range(0, 10)]

    '''
    Check if the number block comprises of only digits
    '''
    def is_number(chunk):
        for c in chunk:
            if c not in digits:
                return False
        return True

    chunks = s.split()
    ret = []
    tmp = []
    for chunk in chunks:
        if is_number(chunk) and len(tmp) < 4:
            tmp.append(chunk)
        else:
            ret.append(tmp)
            tmp = []
    ret.sort(key = lambda x: abs(4-len(x)))
    for r in ret:
        if verify(''.join(r)):
            return r
    return []


def index_view(request):
    data = {}
    return render(request, 'web/index.html', data)

def ocr_view(request):
    data = {}
    try:
        export = json.loads(request.POST['export'])
        img_uri = export['uri'].replace("data:image/jpeg;base64,", "")

        img_uri = base64.b64encode(base64.b64decode(img_uri)).decode('utf-8')
        key = 'AIzaSyAi2_rFWbqdsWl10L_i0pzkTlo98kzEkDA'

        url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBsQnu4Lxmvwmcz6KrpGW3PKldmjR6CCxM'
        payload = {
           "requests": [{
                "image": {
                    "content": img_uri
                },
                "features": [{
                    "type": "TEXT_DETECTION"
                }]
           }]
        }

        headers = {}
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        json_data = json.loads(r.text)

        try:
            full_text = json_data['responses'][0]['fullTextAnnotation']['text']
            data['msg'] = full_text
            card_data = find_credit_num(full_text)
            print(' '.join(card_data))
            if len(card_data) == 4:
                # g = geocoder.ip('me');
                # lat, lon = tuple(g.latlng)
                # lost_url = "http://c6-karma-server.herokuapp.com/alert"
                # lost_payload = {
                #     "location": {
                #         "lat": lat,
                #         "lon": lon
                #     },
                #     "time": str(datetime.datetime.now()),
                #     "card_id": ''.join(card_data),
                #     "status": "N/A"
                # }
                # lost_headers = {}
                # lost_r = requests.post(lost_url, data=json.dumps(lost_payload), headers=lost_headers)
                data['card_data'] = ' '.join(card_data)
                return render(request, 'web/found.html', data)
        except Exception as e:
            print("Error", e)
        return render(request, 'web/index.html', data)
    except Exception as e:
        print("Error", e)
        return render(request, 'web/index.html', data)

