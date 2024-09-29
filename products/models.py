from django.db import models
from vendors.models import Vendor
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, blank=False, null=False)  # Step 1: Add slug field
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.name} ({self.vendor.business_name}) - {self.category}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Auto-generate slug from the name if it's not set
        super().save(*args, **kwargs)

    class StatusChoices(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        UNAVAILABLE = 'Unavailable', 'Unavailable'

    status = models.CharField(max_length=100, choices=StatusChoices.choices)