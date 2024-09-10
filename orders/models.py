from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from customers.models import Userr
from products.models import Product
from enum import Enum
from uuid import uuid4
# Create your models here.


class OrderStatus(Enum):
    CART = 'cart'
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

class Order(models.Model):
    CART_STATUS = OrderStatus.CART.value  # Define CART_STATUS attribute
    PENDING_STATUS = OrderStatus.PENDING.value  # Define PENDING_STATUS attribute
    SHIPPED_STATUS = OrderStatus.SHIPPED.value  # Define SHIPPED_STATUS attribute

    user = models.ForeignKey(Userr, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tracking_number = models.CharField(max_length=255, blank=True, unique=True)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, choices=[(status.value, status.name) for status in OrderStatus])

    def generate_tracking_number(self) -> str:
        """Generate a unique tracking number."""
        return str(uuid4()).replace('-', '').upper()

    def save(self, *args, **kwargs):
        # Generate tracking number only if the status is not 'cart'
        if self.status != self.CART_STATUS and not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        # Check if status is a valid value
        if self.status not in [status.value for status in OrderStatus]:
            raise ValidationError("Invalid status")
        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        # Calculate total amount based on order items
        # This assumes you have an OrderItem model with a price field
        order_items = self.items.all()
        total_amount = sum(item.price for item in order_items)
        return total_amount

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')

    @property
    def price(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)