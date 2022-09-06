from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    question = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    level = models.CharField(max_length=30)
    code = models.TextField()
    pub_date = models.DateTimeField()
    disclosure = models.CharField(max_length=10, null=True) # 공개여부
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True) # 제목
    body = models.TextField(null=True, blank=True) # 본문
    hits = models.PositiveIntegerField(default=0) # 조회수
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return 0
