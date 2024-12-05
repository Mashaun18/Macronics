from django.db import models
from customers.models import Userr
from django.utils.timezone import now, timedelta
# Create your models here.



class Vendor(models.Model):
    user = models.OneToOneField(Userr, on_delete=models.CASCADE, related_name='vendor')
    cac_number = models.CharField(max_length=100, unique=True)
    business_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)     
    address = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    subscription_expiry = models.DateField(blank=True, null=True)  # Monthly subscription
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_subscription_active(self):
        return self.subscription_expiry and self.subscription_expiry > now().date()
    
    def extend_subscription(self):
        """Extend subscription by one month."""
        if self.subscription_expiry and self.subscription_expiry > now().date():
            self.subscription_expiry += timedelta(days=30)
        else:
            self.subscription_expiry = now().date() + timedelta(days=30)
        self.save()

    def __str__(self):
        return f"{self.business_name} ({self.user.username})"










# class Vendor(models.Model):
#     user = models.OneToOneField(Userr, on_delete=models.CASCADE, related_name='vendor')
#     cac_number = models.CharField(max_length=100, unique=True)
#     business_name = models.CharField(max_length=255)
#     contact_phone = models.CharField(max_length=20, blank=True, null=True)    
#     address = models.TextField(blank=True, null=True)
#     verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.business_name} ({self.user.username})"