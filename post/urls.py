from django.urls import path
from . import views

urlpatterns = [
    path('postUpdate', views.postUpdate, name="postUpdate"),
    path('solution', views.getPosts, name="posts"),
    path('solutionDate', views.getPostDate, name="postDate"),
    path('soultion/<int:id>', views.detailPost, name="detail"),
]
