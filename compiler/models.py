from django.db import models

# Create your models here.
class User(models.Model):
    hostname = models.CharField(max_length=100)
    visit = models.IntegerField(default=0)
    current_date = models.DateField(null=True)

    def __str__(self):
        return self.hostname
