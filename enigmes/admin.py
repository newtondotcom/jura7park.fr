from django.contrib import admin
from .models import Enigme

# Register your models here.
@admin.register(Enigme)
class EnigmeAdmin(admin.ModelAdmin):
    list_display = ('numero_enigme', 'reponse', 'user', 'date', 'is_valid')
    list_filter = ('numero_enigme', 'reponse', 'user', 'date', 'is_valid')
    search_fields = ('numero_enigme', 'reponse', 'user', 'date', 'is_valid')
    ordering = ('numero_enigme', 'reponse', 'user', 'date', 'is_valid')