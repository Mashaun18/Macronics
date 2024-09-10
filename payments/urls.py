from django.urls import path
from .views import VerifyPaymentView, initialize_payment

urlpatterns = [
    path('initialize/', initialize_payment, name='initialize-payment'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
