from django.db import models
from catalog.models import Produit

class  achats(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    prix = models.IntegerField(null=True, blank=True,primary_key=False)

