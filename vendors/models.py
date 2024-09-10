from django.db import models
from customers.models import Userr
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(Userr, on_delete=models.CASCADE, related_name='vendor')
    cac_number = models.CharField(max_length=100, unique=True)
    business_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)    
    address = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.business_name} ({self.user.username})"