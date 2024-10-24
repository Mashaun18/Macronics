from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'category', 'stock', 'created_at', 'updated_at', 'image', 'status', 'vendor']
        read_only_fields = ['vendor']  # Vendor should be automatically set and not provided by the user

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        # Assuming vendor is the authenticated user
        validated_data['vendor'] = request.user.vendor  
        return super().create(validated_data)
