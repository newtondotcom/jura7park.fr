from django.db import models

# Create your models here.
class Photo(models.Model):
    MY_CHOICES = (
        ('6', 'Samedi'),
        ('7', 'Dimanche'),
        ('1', 'Lundi'),
        ('2', 'Mardi'),
        ('3', 'Mercredi'),
        ('4', 'Jeudi'),
        ('5', 'Vendredi'),
    )
    jour = models.CharField(max_length=1, choices=MY_CHOICES)
    legende = models.CharField(max_length=500)
    lien = models.CharField(max_length=500)
