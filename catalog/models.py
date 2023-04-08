from django.db import models

class Produit(models.Model):
    title = models.CharField(max_length=100,primary_key=False)
    description = models.TextField()
    price = models.IntegerField(null=True, blank=True,primary_key=False)
    image = models.ImageField(upload_to='')
    stock = models.IntegerField(null=True, blank=True,primary_key=False)

    def __str__(self):
        return self.title