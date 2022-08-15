from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
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
    post_list = Post.objects.all().filter(disclosure='public').order_by('-pub_date')

    qTitle = request.GET.get('qTitle', '')
    if qTitle:
        posts = post_list.filter(Q(question__icontains=qTitle) | Q(category__icontains=qTitle))
    else:
        posts = post_list

    paginator = Paginator(posts, 3)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'FE_templates/search.html', {'posts': posts, 'qTitle': qTitle})

# 전체 풀이 + 날짜 검색
def getPostDate(request):
    post_list = Post.objects.all().filter(disclosure='public').order_by('-pub_date')

    qDate = request.GET.get('qDate', '')
    if qDate:
        posts = post_list.filter(Q(pub_date__icontains=qDate))
    else:
        posts = post_list

    paginator = Paginator(posts, 3)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'FE_templates/search_date.html', {'posts': posts, 'qDate': qDate})

# 풀이 상세
def detailPost(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'FE_templates/detail.html', {'post': post})
