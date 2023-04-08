from django.db import models

# Create your models here.


class events(models.Model):
    time_choices =(
        ('1','Matin'),
        ('2','Midi'),
        ('3','Aprem'),
        ('4','Soir')
    )
    day_CHOICES = (
        ('1', 'Lundi'),
        ('2', 'Mardi'),
        ('3', 'Mercredi'),
        ('4', 'Jeudi'),
        ('5', 'Vendredi'),
        ('6', 'Samedi'),
        ('7', 'Dimanche'),
    )
    jour= models.CharField(choices=day_CHOICES,max_length=1)
    periode=models.CharField(choices=time_choices,max_length=1)
    horaires = models.TextField()
    nom = models.TextField()
    