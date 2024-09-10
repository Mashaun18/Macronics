from django.contrib import admin
from .models import Payment
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'reference', 'amount', 'status', 'created_at')
    search_fields = ('reference', 'order__id')
    list_filter = ['status']

admin.site.register(Payment, PaymentAdmin)