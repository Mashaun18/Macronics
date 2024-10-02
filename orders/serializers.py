from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Order, OrderItem, Product
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'user', 'items', 'shipping_address', 'tracking_number']

class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(write_only=True)  # Items will be passed during order creation

    def save(self, **kwargs):
        with transaction.atomic():
            user = self.context["user"]
            order = Order.objects.create(user=user, status=Order.PENDING_STATUS)

            order_items = []
            for item in self.validated_data['items']:
                product_identifier = item['product']
                product = get_object_or_404(Product, pk=product_identifier) or \
                          get_object_or_404(Product, name=product_identifier) or \
                          get_object_or_404(Product, slug=product_identifier)
            
                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    unit_price=product.price
                )
                order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)
            return order

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]









################################################################
# class OrderItemSerializer(serializers.ModelSerializer):
#     product = serializers.CharField()

#     class Meta:
#         model = OrderItem
#         fields = '__all__'

#     # def get_product_from_data(self, product_data):
#     #     """
#     #     This method checks if the incoming product data is either a pk, name, or slug.
#     #     """
#     #     try:
#     #         # Handle lookup by primary key (int)
#     #         if isinstance(product_data, str) and product_data.isdigit():
#     #             product = Product.objects.filter(pk=int(product_data)).first()
#     #             if not product:
#     #                 raise serializers.ValidationError(f"Product with ID '{product_data}' does not exist.")
#     #             return product
                
#     #         # Handle lookup by unique product name
#     #         elif isinstance(product_data, str):
#     #             products = Product.objects.filter(name=product_data)
#     #             if products.count() == 1:
#     #                 return products.first()
#     #             # Handle lookup by unique slug
#     #             products = Product.objects.filter(slug=product_data)
#     #             if products.count() == 1:
#     #                 return products.first()
            
#     #         raise serializers.ValidationError(f"Multiple or no products found with name/slug '{product_data}'")

#     #     except ValueError:
#     #         raise serializers.ValidationError(f"Invalid product identifier '{product_data}'. It should be an integer, name, or slug.")

#     #     return None

# # class OrderSerializer(serializers.ModelSerializer):
# #     items = OrderItemSerializer(many=True)

# #     class Meta:
# #         model = Order
# #         fields = '__all__'

# #     def create(self, validated_data):
# #         items_data = validated_data.pop('items')
# #         order = Order.objects.create(**validated_data)

# #         for item_data in items_data:
# #             product = self.get_product_from_data(item_data.get('product'))
# #             if product:
# #                 OrderItem.objects.create(order=order, product=product, quantity=item_data.get('quantity'))
# #         return order

# #     def update(self, instance, validated_data):
# #         items_data = validated_data.pop('items', None)

# #         # Update order fields
# #         instance.status = validated_data.get('status', instance.status)
# #         instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
# #         instance.shipping_date = validated_data.get('shipping_date', instance.shipping_date)
# #         instance.save()

# #         if items_data:
# #             for item_data in items_data:
# #                 product = self.get_product_from_data(item_data.get('product'))

# #                 # Try to get the item by ID and update or create a new one if not found
# #                 item_id = item_data.get('id')
# #                 if item_id:
# #                     item = OrderItem.objects.filter(id=item_id, order=instance).first()
# #                     if item and product:
# #                         item.quantity = item_data.get('quantity', item.quantity)
# #                         item.product = product
# #                         item.save()
# #                 else:
# #                     if product:
# #                         OrderItem.objects.create(order=instance, product=product, quantity=item_data.get('quantity'))

# #         return instance

# #     def get_product_from_data(self, product_data):
# #         """
# #         This method checks if the incoming product data is either a pk, name, or slug.
# #         """
# #         try:
# #             # Handle lookup by primary key (int)
# #             if isinstance(product_data, str) and product_data.isdigit():
# #                 product = Product.objects.filter(pk=int(product_data)).first()
# #                 if not product:
# #                     raise serializers.ValidationError(f"Product with ID '{product_data}' does not exist.")
# #                 return product
                
# #             # Handle lookup by unique product name
# #             elif isinstance(product_data, str):
# #                 products = Product.objects.filter(name=product_data)
# #                 if products.count() == 1:
# #                     return products.first()
# #                 # Handle lookup by unique slug
# #                 products = Product.objects.filter(slug=product_data)
# #                 if products.count() == 1:
# #                     return products.first()
            
# #             raise serializers.ValidationError(f"Multiple or no products found with name/slug '{product_data}'")

# #         except ValueError:
# #             raise serializers.ValidationError(f"Invalid product identifier '{product_data}'. It should be an integer, name, or slug.")

# #         return None



# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)
#     class Meta:
#         model = Order 
#         fields = ['id', "created_at", "status", "user", "items", "shipping_address"]
        



# class CreateOrderSerializer(serializers.Serializer):
    
#     def save(self, **kwargs):
#         with transaction.atomic():
#             user = self.context["user"]
#             order = Order.objects.create(user = user)
#             orderitems = [
#                 OrderItem(order=order, 
#                     product=item.product, 
#                     quantity=item.quantity
#                     )
#             for item in orderitems
#             ]
#             OrderItem.objects.bulk_create(orderitems)
#             # Cart.objects.filter(id=cart_id).delete()
#             return order


# class UpdateOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order 
#         fields = ["pending_status"]

###########################



