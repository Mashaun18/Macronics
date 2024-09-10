from django.shortcuts import render
import requests
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from orders.models import Order
from .paystack import Paystack
import uuid
# Create your views here.

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class VerifyPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        reference = request.query_params.get('reference')
        amount = request.query_params.get('amount')

        if not reference or not amount:
            return Response({'detail': 'Reference and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_data = Paystack.verify_payment(reference, amount)
            if payment_data:
                # Update order status and create new payment record
                order_id = payment_data['data']['metadata']['order_id']
                order = Order.objects.get(id=order_id)
                order.status = 'paid'
                order.save()

                Payment.objects.create(
                    order=order,
                    reference=reference,
                    amount=amount,
                    status='success'
                )

                return Response({'status': 'success', 'data': payment_data})
            else:
                return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def initialize_payment(request):
    try:
        amount = request.data.get('amount')
        email = request.data.get('email')
        order_id = request.data.get('order_id')

        if not all([amount, email, order_id]):
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate request data
        if not isinstance(amount, (int, float)) or amount <= 0:
            return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(email, str) or not email:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(order_id, int) or order_id <= 0:
            return Response({'error': 'Invalid order_id'}, status=status.HTTP_400_BAD_REQUEST)

        # Create new payment reference and send request to Paystack API
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'amount': int(float(amount) * 100),
            'email': email,
            'reference': f'{order_id}-{uuid.uuid4().hex}',
            'callback_url': 'https://your-site.com/payment/callback/'
        }

        response = requests.post(f'{Paystack.BASE_URL}/transaction/initialize', headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response(response.json(), status=response.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)