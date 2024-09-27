from rest_framework import serializers
from .models import Order, OrderItem, Product, User
from django.core.exceptions import ObjectDoesNotExist

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            # Handle both pk and string for 'product'
            product = self.get_product_from_data(item_data.get('product'))
            if product:
                OrderItem.objects.create(order=order, product=product, quantity=item_data.get('quantity'))
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        # Update order fields
        instance.status = validated_data.get('status', instance.status)
        instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
        instance.shipping_date = validated_data.get('shipping_date', instance.shipping_date)
        instance.save()

        if items_data:
            for item_data in items_data:
                product = self.get_product_from_data(item_data.get('product'))

                # Try to get the item by ID and update or create a new one if not found
                item_id = item_data.get('id')
                if item_id:
                    item = OrderItem.objects.filter(id=item_id, order=instance).first()
                    if item and product:
                        item.quantity = item_data.get('quantity', item.quantity)
                        item.product = product
                        item.save()
                else:
                    if product:
                        OrderItem.objects.create(order=instance, product=product, quantity=item_data.get('quantity'))

        return instance

    def get_product_from_data(self, product_data):
        """
        This method checks if the incoming product data is either a pk or a unique string field (optional).
        Adjust this function based on your logic.
        """
        try:
            # Check if the product_data is a valid pk (int)
            if isinstance(product_data, int):
                return Product.objects.get(pk=product_data)
            elif isinstance(product_data, str):
                # Handle string case (if you want to identify products by name, SKU, etc.)
                # If no such string identifier exists, remove this clause and keep pk-only lookup.
                return Product.objects.get(name=product_data)  # Assuming 'name' is unique (change as necessary)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Product with identifier '{product_data}' does not exist.")

        return None

