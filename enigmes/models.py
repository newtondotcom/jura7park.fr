from django.db import models

# Create your models here.
class Enigme(models.Model):
    numero_enigme = models.IntegerField()
    reponse = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=False)
    
