from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from member.forms import UserForm
from compiler.forms import CodeExecutorForm

from post.models import Post
from compiler.models import UserCheck
from problem.models import Problem, Example

from problem.views import crawling

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
    return render(request, 'FE_tamplates/mypage.html', {'data':data, 'post_list': post_list})

def submitCodeIncorrect(request):
    if request.user.is_authenticated:
        login_user = request.user

    incorrect_list = UserCheck.objects.all().filter(user=login_user, is_correct=0)
    for usercheck in incorrect_list:
        print(usercheck.problem.id, '!!')
    # print(incorrect_list.get().problem)
    # print(incorrect_list, '!!!!!!!!!!!')

    # post_list = Post.objects.all().filter(writer=login_user).order_by('-pub_date')

    # paginator1 = Paginator(post_list, 9)
    # pagenum = request.GET.get('page')
    # post_list=paginator1.get_page(pagenum)
    data = {
        'username': login_user.username,
        'email': login_user.email
    }
    return render(request, 'member/incorrectCode.html', {'data':data, 'incorrect_list': incorrect_list})
    # return render(request, 'FE_tamplates/mypage.html', {'data':data, 'incorrect_list': incorrect_list})

def retryCode(request, id):
    problem = get_object_or_404(Problem, pk=id)
    example = Example.objects.all().filter(problem=problem).get()
    # parsing
    example_input = example.example_input.split('\'')
    del example_input[0::2]
    example_output = example.example_output.split('\'')
    del example_output[0::2]

    form = CodeExecutorForm()
    template_data = {}
    template_data['form'] = form

    level = problem.problem_level

    return render(request, 'FE_templates/index.html',
    {
        'level': level,
        'form': template_data['form'],
        'problem_title': problem.problem_title,
        'problem_description': problem.problem_text,
        'problem_input': problem.problem_input,
        'problem_output': problem.problem_output,
        'problem_sample_input': example_input,
        'problem_sample_output': example_output
    })

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

