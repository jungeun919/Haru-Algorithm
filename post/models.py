from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem

# Create your models here.
class Post(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    code = models.TextField()
    pub_date = models.DateTimeField()
    disclosure = models.CharField(max_length=10, null=True) # 공개여부
    writer = models.ForeignKey(User, related_name='writer', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True) # 제목
    body = models.TextField(null=True, blank=True) # 본문
    hits = models.PositiveIntegerField(default=0) # 조회수
    like_users = models.ManyToManyField(User, related_name='likes', blank=True)
    likes = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 0
