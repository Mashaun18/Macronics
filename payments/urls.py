from django.urls import path
from .views import VerifyPaymentView, initialize_payment, payment_callback

urlpatterns = [
    path('initialize/', initialize_payment, name='initialize-payment'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('callback/', payment_callback, name='payment-callback'),
]
