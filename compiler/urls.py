# from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    re_path(r'^compiler$', views.runCode, name="compiler"),
]
