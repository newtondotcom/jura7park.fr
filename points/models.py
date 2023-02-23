from django.db import models
from django.contrib.auth.models import User

class points(models.Model):
    #surnom = models.CharField(max_length=100)
    surnom = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    point = models.IntegerField()
    avatar = models.TextField()
    nomavatar = models.TextField(null=True, blank=True)

