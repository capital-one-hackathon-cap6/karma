from django.conf.urls import url

from . import views

app_name = 'web'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^ocr/$', views.ocr_view, name='ocr')
]