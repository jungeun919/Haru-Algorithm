from django.db import models

# Create your models here.
class Post(models.Model):
    question = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    code = models.TextField()
    pub_date = models.DateTimeField()
    disclosure = models.CharField(max_length=10, null=True) # 공개여부
    
    def __str__(self):
        return self.question
