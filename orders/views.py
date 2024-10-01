from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer

class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "patch", "post", "delete", "options", "head"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={"user": self.request.user})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

@api_view(['PATCH'])
def update_order_status(request, pk):
    try:
        order = get_object_or_404(Order, pk=pk)
        status_value = request.data.get('status')

        if not status_value or status_value not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid or missing status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save()
        return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def cart_details(request):
    user = request.user
    cart = Order.objects.filter(user=user, status=Order.CART_STATUS).first()
    if not cart:
        return Response({'message': 'No active cart'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(cart)
    return Response(serializer.data)

@api_view(['GET'])
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).exclude(status=Order.CART_STATUS)

    if not orders.exists():
        return Response({'message': 'No order history found'}, status=status.HTTP_404_NOT_FOUND)

    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_orders = paginator.paginate_queryset(orders, request)

    serializer = OrderSerializer(paginated_orders, many=True)
    return paginator.get_paginated_response(serializer.data)
