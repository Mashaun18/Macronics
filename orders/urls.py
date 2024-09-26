from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, cart_details, order_history

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', cart_details, name='cart_details'),
    path('history/', order_history, name='order_history'),
]