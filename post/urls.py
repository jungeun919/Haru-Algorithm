from django.urls import path
from . import views

urlpatterns = [
    path('postUpdate', views.postUpdate, name="postUpdate"),
    path('solution', views.getPosts, name="posts"),
    path('solutionDate', views.getPostDate, name="postDate"),
    path('solutionLevel', views.getPostLevel, name="postLevel"),
    path('soultion/<int:id>', views.detailPost, name="detail"),
    path('solution/<int:id>/like', views.likes, name="likes"),
]
