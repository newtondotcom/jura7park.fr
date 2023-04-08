from django.db import models

# Create your models here.
class repenigmes(models.Model):
    day_CHOICES = (
        ('3', 'Lundi'),
        ('4', 'Mardi'),
        ('5', 'Mercredi'),
        ('6', 'Jeudi'),
        ('7', 'Vendredi'),
        ('1', 'Samedi'),
        ('2', 'Dimanche'),
    )
    numero_enigme = models.CharField(choices=day_CHOICES,max_length=1)
    reponse = models.CharField(max_length=200)
    indice = models.TextField(null=True,blank=True)