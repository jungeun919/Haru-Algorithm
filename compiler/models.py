from django.db import models
from problem.models import Problem
from django.contrib.auth.models import User

# Create your models here.
class UserCheck(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    # username = models.CharField(max_length=100)
    fail = models.IntegerField(default=0) # 실패 횟수
    current_date = models.DateField(null=True)
    level = models.CharField(max_length=30)
    is_correct = models.PositiveIntegerField(default=0) # 정답 여부 (정답: 1, 오답: 0)

    def __str__(self):
        return self.user.username
