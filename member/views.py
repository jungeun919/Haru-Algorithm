from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from member.forms import UserForm
from post.models import Post
from django.core.paginator import Paginator
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
    return render(request, 'FE_tamplates/singup.html', {'form': form})

# def mypage(request):
#     if request.user.is_authenticated:
#         login_user = request.user
    
#     post_correct_list = Post.objects.all().filter(writer=login_user).order_by('-pub_date')
#     post_like_list = Post.objects.all().filter(like_users__in=[login_user]).order_by('-pub_date')
    

#     paginator2=Paginator( post_like_list, 9)
#     pagenum = request.GET.get('page')
#     post_like_list=paginator2.get_page(pagenum)
#     data = {
#         'username': login_user.username,
#         'email': login_user.email
#     }
#     return render(request, 'FE_tamplates/mypage.html', {'data':data,'post_correct_list': post_correct_list,'post_like_list':post_like_list})

def submitCodeCorrect(request):
    if request.user.is_authenticated:
        login_user = request.user

    post_list = Post.objects.all().filter(writer=login_user).order_by('-pub_date')

    paginator1 = Paginator(post_list, 9)
    pagenum = request.GET.get('page')
    post_list=paginator1.get_page(pagenum)
    data = {
        'username': login_user.username,
        'email': login_user.email
    }    
    return render(request, 'FE_tamplates/mypage.html', {'data':data,'post_list': post_list})

def likePost(request):
    if request.user.is_authenticated:
        login_user = request.user

    post_list = Post.objects.all().filter(like_users__in=[login_user]).order_by('-pub_date')
    
    paginator1 = Paginator(post_list, 9)
    pagenum = request.GET.get('page')
    post_list=paginator1.get_page(pagenum)
    data = {
        'username': login_user.username,
        'email': login_user.email
    }
    return render(request, 'FE_tamplates/likePost.html', {'data':data,'post_list': post_list})

