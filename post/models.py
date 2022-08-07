from django.db import models

# Create your models here.
class Post(models.Model):
    question = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    code = models.TextField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.question
