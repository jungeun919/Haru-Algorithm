from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from member.forms import UserForm
from post.models import Post

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'member/signup.html', {'form': form})

def mypage(request):
    if request.user.is_authenticated:
        login_user = request.user
    
    data = {
        'username': login_user.username,
        'email': login_user.email
    }
    return render(request, 'member/mypage.html', data)

def submitCodeCorrect(request):
    if request.user.is_authenticated:
        login_user = request.user

    post_list = Post.objects.all().filter(writer=login_user).order_by('-pub_date')
    return render(request, 'member/correctCode.html', {'post_list': post_list})

def likePost(request):
    if request.user.is_authenticated:
        login_user = request.user

    post_list = Post.objects.all().filter(like_users__in=[login_user]).order_by('-pub_date')
    return render(request, 'member/likePost.html', {'post_list': post_list})

