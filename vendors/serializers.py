from rest_framework import serializers
from .models import Vendor
from customers.serializers import UserSerializer       


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subscription_active = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = ['id', 'user', 'cac_number', 'business_name', 'contact_phone', 'address', 'verified', 'listing_fee_paid', 'subscription_expiry', 'subscription_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'subscription_active']

    def get_subscription_active(self, obj):
        return obj.is_subscription_active()
