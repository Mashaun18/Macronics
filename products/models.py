from django.db import models
from vendors.models import Vendor
# Create your models here.

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.name} ({self.vendor.business_name}) - {self.category}"

    class StatusChoices(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        UNAVAILABLE = 'Unavailable', 'Unavailable'

    status = models.CharField(max_length=100, choices=StatusChoices.choices)