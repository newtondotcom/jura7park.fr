from django.db import models

# Create your models here.
class Stock(models.Model):
    surnom = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    avatar = models.TextField()
    nomavatar = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)