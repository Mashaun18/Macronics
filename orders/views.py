from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user:
            return Order.objects.filter(user=user)
        else:
            return Order.objects.none()

    def perform_create(self, serializer):
        order = serializer.save()
        # Add some logic here to handle the newly created order

    def update_order_status(self, request, pk, status):
        try:
            order = self.get_object()
            order.status = status
            order.save()
            return Response({'message': 'Order status updated successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)