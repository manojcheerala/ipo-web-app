# Register your models here.
from django.contrib import admin
from .models import IPO

@admin.register(IPO)
class IPOAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'status', 'open_date', 'close_date', 'listing_date')
    list_filter = ('status',)
    search_fields = ('company_name',)