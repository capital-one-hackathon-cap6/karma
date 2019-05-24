import json
import random
import string
import io
import os

import requests
import base64

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User

def index_view(request):
    data = {}
    return render(request, 'web/index.html', data)

def ocr_view(request):
    data = {}
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
    # print(json.dumps(str(r.content)))
    json_data = json.loads(r.text)

    # for text in json_data['responses'][0]['textAnnotations']:
    #     print(text['description'])

    try:
        print(json_data['responses'][0]['fullTextAnnotation']['text'])
        data['messages'] = json_data['responses'][0]['fullTextAnnotation']['text']
    except Exception as e:
        print("Error", e)
    
    # print(json_data['responses'][0].keys())

    return render(request, 'web/index.html', data)
