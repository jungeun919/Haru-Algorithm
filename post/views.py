from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post
from django.db.models import Q

# 공개 여부 업데이트 (default : private)
# compiler/template/result.html에서 호출
def postUpdate(request):
    disclosure = request.GET.get('disclosure') # 1: public, 2: private
    post_id = request.GET.get('post_id')

    if (disclosure == '1'):
        update_post = Post.objects.get(id=post_id)
        update_post.question = request.GET.get('question')
        update_post.category = request.GET.get('category')
        update_post.code = request.GET.get('code')
        update_post.pub_date = timezone.now()
        update_post.disclosure = 'public'
        title = request.GET.get('title')
        if title:
            update_post.title = title
        else:
            update_post.title = 'Unnamed Title'
        body = request.GET.get('body')
        if body:
            update_post.body = body
        else:
            update_post.body = 'Body is empty.'
        update_post.save()
    return redirect('posts')

# 전체 풀이 + 제목 검색
def getPosts(request):
    sort = request.GET.get('sort', '')
    if sort == 'likes':
        post_list = Post.objects.all().filter(disclosure='public').order_by('-likes', '-pub_date')
    elif sort == 'hits':
        post_list = Post.objects.all().filter(disclosure='public').order_by('-hits', '-pub_date')
    else:
        post_list = Post.objects.all().filter(disclosure='public').order_by('-pub_date')

    qTitle = request.GET.get('qTitle', '')
    if qTitle:
        posts = post_list.filter(Q(title__icontains=qTitle))
    else:
        posts = post_list


    paginator = Paginator(posts, 4)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'FE_templates/search.html', {'posts': posts, 'qTitle': qTitle})

# 전체 풀이 + 날짜 검색
def getPostDate(request):
    sort = request.GET.get('sort', '')
    if sort == 'likes':
        post_list = Post.objects.all().filter(disclosure='public').order_by('-likes', '-pub_date')
    elif sort == 'hits':
        post_list = Post.objects.all().filter(disclosure='public').order_by('-hits', '-pub_date')
    else:
        post_list = Post.objects.all().filter(disclosure='public').order_by('-pub_date')
    
    qDate = request.GET.get('qDate', '')
    if qDate:
        posts = post_list.filter(Q(pub_date__icontains=qDate))
    else:
        posts = post_list

    paginator = Paginator(posts, 4)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'FE_templates/search_date.html', {'posts': posts, 'qDate': qDate})

# 전체 풀이 + 레벨 검색
def getPostLevel(request):
    sort = request.GET.get('sort', '')
    if sort == 'likes':
        post_list = Post.objects.all().filter(disclosure='public').order_by('-likes', '-pub_date')
    elif sort == 'hits':
        post_list = Post.objects.all().filter(disclosure='public').order_by('-hits', '-pub_date')
    else:
        post_list = Post.objects.all().filter(disclosure='public').order_by('-pub_date')

    qLevel = request.GET.get('qLevel', '')
    if qLevel:
        posts = post_list.filter(Q(problem__problem_level__icontains=qLevel))
    else:
        posts = post_list

    paginator = Paginator(posts, 4)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'FE_templates/search_level.html', {'posts': posts, 'qLevel': qLevel})

# 풀이 상세
def detailPost(request, id):
    post = get_object_or_404(Post, pk=id)

    # 쿠키 이용하여 조회수
    expire_date, now = datetime.now(), datetime.now() # 2022-09-06 14:51:16
    expire_date += timedelta(days=1) # 2022-09-07 14:51:16
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0) # 2022-09-07 00:00:00
    expire_date -= now # 9:08:44.597768
    max_age = expire_date.total_seconds() # 남은 시간을 초로 환산

    cookie_value = request.COOKIES.get('hitboard', '_')
    response = render(request, 'FE_templates/detail.html', {'post': post})

    if f'_{id}_' not in cookie_value:
        cookie_value += f'{id}_'
        response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
        post.hits += 1
        post.save()
    return response

# 좋아요
def likes(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=id)

        if post.like_users.filter(pk=request.user.pk).exists():
            post.like_users.remove(request.user)
            post.likes -= 1
            post.save()
        else:
            post.like_users.add(request.user)
            post.likes += 1
            post.save()
        return HttpResponseRedirect(reverse('detail', args=[str(id)]))
    return redirect('login')
