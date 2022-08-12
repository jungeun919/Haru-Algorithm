from django.urls import URLPattern, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.problem, name='problem'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

