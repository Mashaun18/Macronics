from rest_framework import serializers
from .models import Vendor
from customers.serializers import UserSerializer

class VendorSerializer(serializers.ModelSerializer):
    """
    Vendor serializer for serializing and deserializing vendor data.
    """
    user = UserSerializer(read_only=True)
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'cac_number', 'business_name', 'contact_phone', 'address', 'verified', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']        