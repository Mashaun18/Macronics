from django.contrib import admin
from .models import Order, OrderItem
from orders import models
# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of extra forms to display
    verbose_name = 'Order Item'
    verbose_name_plural = 'Order Items'

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'tracking_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return Order.objects.filter(status='pending')

    def save_model(self, request, obj, form, change):
        # Perform custom actions here
        super().save_model(request, obj, form, change)

admin.site.register(Order, OrderModelAdmin)