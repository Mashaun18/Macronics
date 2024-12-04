from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
    # path('pay-listing-fee/', pay_listing_fee, name='pay-listing-fee'),
    # path('verify-listing-payment/', verify_listing_payment, name='verify-listing-payment'),