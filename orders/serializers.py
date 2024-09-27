from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        # Optionally mark `order` as read-only if it should not be explicitly set
        # read_only_fields = ['order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Extract related items data
        order = Order.objects.create(**validated_data)  # Create order instance

        # Create order items for the order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        # Update order fields
        instance.status = validated_data.get('status', instance.status)
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.shipping_date = validated_data.get('shipping_date', instance.shipping_date)
        instance.save()

        # If items_data is provided, update or create related order items
        if items_data:
            for item_data in items_data:
                # Try to get the item by ID and update or create a new one if not found
                item_id = item_data.get('id')
                if item_id:
                    item = OrderItem.objects.filter(id=item_id, order=instance).first()
                    if item:
                        item.quantity = item_data.get('quantity', item.quantity)
                        item.product = item_data.get('product', item.product)
                        item.save()
                else:
                    OrderItem.objects.create(order=instance, **item_data)

        return instance
