from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('aboutus',views.aboutus, name='aboutus'),
    url(r'^compiler$', views.runCode, name="compiler"),
]
