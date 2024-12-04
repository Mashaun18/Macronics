from django.contrib import admin
from .models import Vendor

# Register your models here.
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'contact_phone', 'verified', 'created_at', 'listing_fee_paid', 'subscription_expiry', 'subscription_active')
    search_fields = ('business_name', 'user__username', 'cac_number', 'listing_fee_paid', 'subscription_expiry', 'subscription_active')
    list_filter = ('verified', 'created_at', 'listing_fee_paid', 'subscription_expiry', 'subscription_active')
    fields = ('business_name', 'user', 'cac_number', 'contact_phone', 'address', 'verified')

    # Add a custom action to verify vendors
    actions = ['verify_vendors']

    def verify_vendors(self, request, queryset):
        updated = queryset.update(verified=True)  # Mark selected vendors as verified
        self.message_user(request, f'{updated} vendor(s) successfully verified.')
    verify_vendors.short_description = 'Verify selected vendors'
