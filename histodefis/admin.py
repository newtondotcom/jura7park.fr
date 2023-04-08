from django.contrib import admin
from .models import histodinos

# Register your models here.
@admin.register(histodinos)
class histodinosAdmin(admin.ModelAdmin):
    list_display = ['defi', 'beneficaire', 'montant', 'payeur','date']
    list_filter = ['defi', 'beneficaire', 'montant', 'payeur','date']
    search_fields = ['defi', 'beneficaire', 'montant', 'payeur','date']
    ordering = ['defi', 'beneficaire', 'montant', 'payeur','date']
