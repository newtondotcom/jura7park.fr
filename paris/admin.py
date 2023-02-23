from django.contrib import admin
from .models import paris

# Register your models here.
@admin.register(paris)
class parisAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'mise', 'gagnant','is_paid')
    list_filter = ('user', 'date', 'mise', 'gagnant')
    search_fields = ('user', 'date', 'mise', 'gagnant')
    ordering = ('user', 'date', 'mise', 'gagnant')