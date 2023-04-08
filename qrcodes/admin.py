from django.contrib import admin
from .models import codeqr

@admin.register(codeqr)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('title', 'datecreation', 'dateutil', 'createur', 'utilisateur', 'points', 'utilise', 'code','nb_utilisation')
    list_filter=('utilise','dateutil', 'datecreation','nb_utilisation')
    ordering = ('points',)

