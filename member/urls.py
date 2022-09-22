from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'member'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='FE_tamplates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name="mypage"),
    path('mypage/submitCodeCorrect/', views.submitCodeCorrect, name="submitCodeCorrect"),
    path('mypage/submitCodeIncorrect/', views.submitCodeIncorrect, name="submitCodeIncorrect"),
    path('mypage/retryCode/<int:id>', views.retryCode, name="retryCode"),
    path('mypage/likePost/', views.likePost, name="likePost"),
]
