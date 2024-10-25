from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from customers.models import UserRole
from .models import Vendor
from .serializers import VendorSerializer

# Create your views here.

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserRole.VENDOR:
            return Vendor.objects.filter(user=user)
        return Vendor.objects.all()