from django.contrib import admin
from .models import Produit

@admin.register(Produit)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'stock')
    ordering = ('price',)
