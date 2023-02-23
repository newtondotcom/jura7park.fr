from django.contrib import admin
from .models import points

@admin.register(points)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('surnom', 'point', 'avatar')
