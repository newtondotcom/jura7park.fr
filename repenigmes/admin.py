from django.contrib import admin
from .models import repenigmes

# Register your models here.
@admin.register(repenigmes)
class repenigmesAdmin(admin.ModelAdmin):
    list_display = ('numero_enigme', 'reponse')
    list_filter = ('numero_enigme', 'reponse')
    search_fields = ('numero_enigme', 'reponse')
    ordering = ('numero_enigme', 'reponse')