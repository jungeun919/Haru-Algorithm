from django.db import models

# Create your models here.
class Level(models.Model):
    bronze = models.TextField(null=True)
    silver = models.TextField(null=True)
    gold = models.TextField(null=True)
    platinum = models.TextField(null=True)
    diamond = models.TextField(null=True)
    ruby = models.TextField(null=True) 

class Problem(models.Model):
    problem_date = models.DateField(null=True)
    problem_num = models.IntegerField(unique=True, null=True)
    problem_category = models.CharField(max_length=30, null=True)
    problem_level = models.CharField(max_length=30, null=True, blank=True)
    problem_title = models.TextField(null=True)
    problem_text = models.TextField(null=True, blank=True)
    problem_input = models.TextField(null=True)
    problem_output = models.TextField(null=True)

    def __str__(self):
        return self.problem_title

class Example(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    example_input = models.TextField(null=True)
    example_output = models.TextField(null=True)

    def __str__(self):
        return self.problem.problem_title
