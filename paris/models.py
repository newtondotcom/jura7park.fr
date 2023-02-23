from django.db import models

# Create your models here.
class paris(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    mise = models.IntegerField()
    gagnant = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username