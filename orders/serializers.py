from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.status = validated_data.get('status', instance.status)
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.shipping_date = validated_data.get('shipping_date', instance.shipping_date)
        instance.save()

        # Update or create order items
        for item_data in items_data:
            item_id = item_data.get('id', None)
            if item_id:
                try:
                    item = OrderItem.objects.get(id=item_id, order=instance)
                    item.quantity = item_data.get('quantity', item.quantity)
                    item.save()
                except OrderItem.DoesNotExist:
                    # Handle the case when the item does not exist
                    pass
            else:
                OrderItem.objects.create(order=instance, **item_data)

        return instance