from django.db import models
from orders.models import Order
# Create your models here.

class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payment', on_delete=models.CASCADE)
    reference = models.CharField(max_length=555, unique=True)
    amount = models.IntegerField()  # Amount in kobo
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.reference} - Order {self.order.id}'