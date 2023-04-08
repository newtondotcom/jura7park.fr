from django.db import models

class codeqr(models.Model):
    title = models.CharField(max_length=100)
    datecreation = models.DateTimeField(auto_now_add=True)
    dateutil = models.DateTimeField(null=True, blank=True)
    createur = models.ForeignKey('auth.User', related_name='creat_codeqr', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey('auth.User', related_name='user_codeqr', on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField()
    utilise = models.BooleanField()
    code=models.CharField(max_length=100,null=True, blank=True)
    nb_utilisation = models.IntegerField(default=1)
    lien = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.title