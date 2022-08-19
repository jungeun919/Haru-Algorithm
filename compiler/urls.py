# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('compiler', views.runCode, name="compiler"),
]
