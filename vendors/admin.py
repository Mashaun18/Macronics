from django.contrib import admin
from .models import Vendor
# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'contact_phone', 'verified', 'created_at')
    search_fields = ('business_name', 'user__username', 'cac_number')
    list_filter = ('verified', 'created_at')
    fields = ('business_name', 'user', 'cac_number', 'contact_phone', 'address')