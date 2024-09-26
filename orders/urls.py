from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, cart_details, order_history

router = DefaultRouter()
router.register(r'orders', OrderViewSet)  # Register only the OrderViewSet

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
    path('cart/', cart_details, name='cart_details'),  # Separate path for cart details
    path('history/', order_history, name='order_history'),  # Separate path for order history
]
