from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('alert', views.receive_alert, name='receive_alert'),
    path('alert_callback', views.alert_callback, name='alert_callback'),
]
