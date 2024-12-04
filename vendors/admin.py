from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'contact_phone', 'verified', 'created_at', 'listing_fee_paid', 'subscription_expiry', 'subscription_active')
    search_fields = ('business_name', 'user__username', 'cac_number', 'listing_fee_paid')
    list_filter = ('verified', 'created_at', 'listing_fee_paid', 'subscription_expiry')
    fields = ('business_name', 'user', 'cac_number', 'contact_phone', 'address', 'verified')
    actions = ['verify_vendors']

    def subscription_active(self, obj):
        return obj.is_subscription_active()
    subscription_active.boolean = True
    subscription_active.short_description = 'Subscription Active'

    def verify_vendors(self, request, queryset):
        unverified_vendors = queryset.filter(verified=False)
        updated = unverified_vendors.update(verified=True)
        self.message_user(request, f'{updated} vendor(s) successfully verified.')
