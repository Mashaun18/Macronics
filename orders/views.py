from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the order with the current user
        serializer.save(user=self.request.user)
        # Product and item creation logic is handled inside the serializer now

@api_view(['PATCH'])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        status_value = request.data.get('status')

        if not status_value:
            return Response({'error': 'No status provided'}, status=status.HTTP_400_BAD_REQUEST)

        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status provided'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save()
        return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)

    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def cart_details(request):
    user = request.user
    cart = Order.objects.filter(user=user, status='cart').first()
    if not cart:
        return Response({'message': 'No active cart'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).exclude(status='cart')

    if not orders.exists():
        return Response({'message': 'No order history found'}, status=status.HTTP_404_NOT_FOUND)

    # Use pagination
    paginator = PageNumberPagination()
    paginator.page_size = 20  # Adjust the page size as needed
    paginated_orders = paginator.paginate_queryset(orders, request)

    serializer = OrderSerializer(paginated_orders, many=True)
    return paginator.get_paginated_response(serializer.data)
