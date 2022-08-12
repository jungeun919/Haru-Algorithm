from asyncio.windows_events import NULL
from django.db import models

# Create your models here.
class Post(models.Model):
    question = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    code = models.TextField()
    pub_date = models.DateTimeField()
    disclosure = models.CharField(max_length=10, null=True) # 공개여부
    title = models.CharField(max_length=50, null=True, blank=True) # 제목
    body = models.TextField(null=True, blank=True) # 본문
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return NULL
