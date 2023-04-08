from django.contrib import admin
from .models import Stock

# Register your models here.
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('surnom', 'avatar', 'nomavatar', 'date')
    list_filter = ('surnom', 'avatar', 'nomavatar', 'date')
    search_fields = ('surnom', 'avatar', 'nomavatar', 'date')
    ordering = ('surnom', 'avatar', 'nomavatar', 'date')