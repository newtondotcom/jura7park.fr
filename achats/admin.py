from django.contrib import admin
from .models import achats

@admin.register(achats)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('produit', 'user','date', 'prix')
