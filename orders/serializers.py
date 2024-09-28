from rest_framework import serializers
from .models import Order, OrderItem, Product
from django.core.exceptions import ObjectDoesNotExist

class OrderItemSerializer(serializers.ModelSerializer):
    # Change product to a CharField to allow both string and int inputs
    product = serializers.CharField()

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
            # Retrieve product using get_product_from_data method
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
        This method checks if the incoming product data is either a pk or a unique string field (e.g., product name).
        Adjust this function based on your logic.
        """
        try:
            # Handle lookup by primary key (int)
            if product_data.isdigit():
                return Product.objects.get(pk=int(product_data))
            
            # Handle lookup by unique product name
            elif isinstance(product_data, str):
                products = Product.objects.filter(name=product_data)
                if products.count() == 1:
                    return products.first()
                else:
                    raise serializers.ValidationError(f"Multiple or no products found with name '{product_data}'")
        except ObjectDoesNotExist:
            raise serializers.ValidationError(f"Product with identifier '{product_data}' does not exist.")

        return None
