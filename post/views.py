from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Post
from django.db.models import Q

# 전체 풀이 + 제목 검색
def getPosts(request):
    post_list = Post.objects.all().order_by('-pub_date')

    qTitle = request.GET.get('qTitle', '')
    if qTitle:
        posts = post_list.filter(Q(question__icontains=qTitle) | Q(category__icontains=qTitle))
    else:
        posts = post_list

    paginator = Paginator(posts, 3)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'post/posts.html', {'posts': posts, 'qTitle': qTitle})

# 전체 풀이 + 날짜 검색
def getPostDate(request):
    post_list = Post.objects.all().order_by('-pub_date')

    qDate = request.GET.get('qDate', '')
    if qDate:
        posts = post_list.filter(Q(pub_date__icontains=qDate))
    else:
        posts = post_list

    paginator = Paginator(posts, 3)
    pagenum = request.GET.get('page')
    posts = paginator.get_page(pagenum)
    return render(request, 'post/postDate.html', {'posts': posts, 'qDate': qDate})

# 풀이 상세
def detailPost(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'post/detail.html', {'post': post})
