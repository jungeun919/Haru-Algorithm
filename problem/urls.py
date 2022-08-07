from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('problem/', views.problem, name='problem'),
]