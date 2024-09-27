from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()

    def perform_create(self, serializer):
        # Automatically associate the order with the current user
        serializer.save(user=self.request.user)  # Save the order with the user
        # Add additional logic here if needed, e.g., sending notifications

@api_view(['PATCH'])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        status = request.data.get('status')
        if status:
            order.status = status
            order.save()
            return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'No status provided'}, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def cart_details(request):
    user = request.user
    cart = Order.objects.filter(user=user, status='cart').first()  # Assuming 'cart' indicates a cart
    if cart:
        serializer = OrderSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'No active cart'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).exclude(status='cart')  # Exclude cart status to show completed orders
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
