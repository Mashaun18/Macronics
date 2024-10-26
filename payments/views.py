import json
from django.conf import settings
import requests
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import PaymentSerializer
from orders.models import Order
from .paystack import Paystack
import uuid
import logging

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class VerifyPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        reference = request.query_params.get('reference')
        amount = request.query_params.get('amount')

        logger.info("Received request with reference: %s", reference)

        if not reference or not amount:
            logger.warning("Reference or amount missing.")
            return Response({'detail': 'Reference and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        paystack = Paystack()
        payment_data = paystack.verify_payment(reference)

        logger.info("Payment data from Paystack: %s", payment_data)

        if payment_data.get('status') == 'success':
            data = payment_data['data']
            
            # Check if metadata exists and contains the order_id
            metadata = data.get('metadata', {})
            if isinstance(metadata, str):
                metadata = {}

            order_id = metadata.get('order_id')

            # Log a warning if order_id is missing, and handle the case
            if not order_id:
                logger.warning("Order ID is missing in payment metadata. Proceeding without updating the order.")
                # If your application allows payments without order linkage, continue processing
                return Response({'status': 'success', 'data': payment_data})
            
            try:
                order = get_object_or_404(Order, id=order_id)
                order.status = 'paid'
                order.save()

                Payment.objects.create(
                    order=order,
                    reference=reference,
                    amount=int(amount),  # Ensure this is an integer
                    status='success'
                )

                return Response({'status': 'success', 'data': payment_data})

            except Exception as e:
                logger.error("Error processing order: %s", str(e))
                return Response({'status': 'failed', 'detail': 'Could not find or update order.'}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.error("Verification failed: %s", payment_data)
        return Response({'status': 'failed', 'detail': payment_data.get('message', 'Unknown error occurred.')}, 
                        status=status.HTTP_400_BAD_REQUEST)




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

        reference = f'{order_id}-{uuid.uuid4().hex}'
        payload = {
            'amount': int(float(amount) * 100),  # Convert to kobo
            'email': email,
            'reference': reference,
            'callback_url': 'https://macronics.onrender.com/api/payments/callback/'
        }

        response = requests.post(f'{Paystack.BASE_URL}/transaction/initialize', headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return Response({'data': data, 'order_id': order_id})
        else:
            logger.error(f"Error initializing payment: {response.json()}")
            return Response({'error': response.json().get('message', 'Error initializing payment')}, status=response.status_code)
    except Exception as e:
        logger.error(f"Error initializing payment: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return Response({'error': 'No reference provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Verify payment using Paystack
        paystack = Paystack()
        payment_data = paystack.verify_payment(reference)

        if isinstance(payment_data, dict) and payment_data.get('status'):
            order_id = payment_data['data']['metadata']['order_id']
            order = get_object_or_404(Order, id=order_id)
            order.status = 'paid'
            order.save()

            return Response({'status': 'success', 'message': 'Payment verified successfully'})
        else:
            logger.error("Payment verification failed: %s", payment_data)
            return Response({'status': 'failed', 'message': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in payment callback: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






# from django.shortcuts import render
# import requests
# from django.conf import settings
# from rest_framework import viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from .models import Payment
# from .serializers import PaymentSerializer
# from orders.models import Order
# from .paystack import Paystack
# import uuid

# # Create your views here.

# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

# class VerifyPaymentView(APIView):
#     def get(self, request, *args, **kwargs):
#         reference = request.query_params.get('reference')
#         amount = request.query_params.get('amount')

#         if not reference or not amount:
#             return Response({'detail': 'Reference and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             payment_data = Paystack.verify_payment(reference, amount)
#             if payment_data:
#                 # Update order status and create new payment record
#                 order_id = payment_data['data']['metadata']['order_id']
#                 order = Order.objects.get(id=order_id)
#                 order.status = 'paid'
#                 order.save()

#                 Payment.objects.create(
#                     order=order,
#                     reference=reference,
#                     amount=amount,
#                     status='success'
#                 )

#                 return Response({'status': 'success', 'data': payment_data})
#             else:
#                 return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def initialize_payment(request):
#     try:
#         amount = request.data.get('amount')
#         email = request.data.get('email')
#         order_id = request.data.get('order_id')

#         if not all([amount, email, order_id]):
#             return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

#         # Validate request data
#         if not isinstance(amount, (int, float)) or amount <= 0:
#             return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)

#         if not isinstance(email, str) or not email:
#             return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

#         if not isinstance(order_id, int) or order_id <= 0:
#             return Response({'error': 'Invalid order_id'}, status=status.HTTP_400_BAD_REQUEST)

#         # Create new payment reference and send request to Paystack API
#         headers = {
#             'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
#             'Content-Type': 'application/json'
#         }

#         payload = {
#             'amount': int(float(amount) * 100),  # Convert to kobo
#             'email': email,
#             'reference': f'{order_id}-{uuid.uuid4().hex}',
#             'callback_url': 'https://macronics.onrender.com/api/payments/callback/'  # Updated with your render domain
#         }

#         response = requests.post(f'{Paystack.BASE_URL}/transaction/initialize', headers=headers, json=payload)

#         if response.status_code == 200:
#             data = response.json()
#             return Response(data)
#         else:
#             return Response(response.json(), status=response.status_code)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# def payment_callback(request):
#     reference = request.GET.get('reference')
#     if not reference:
#         return Response({'error': 'No reference provided'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Verify payment using Paystack
#         paystack = Paystack()
#         payment_data = paystack.verify_payment(reference)

#         if payment_data:
#             # Update order/payment status
#             order_id = payment_data['data']['metadata']['order_id']
#             order = Order.objects.get(id=order_id)
#             order.status = 'paid'
#             order.save()

#             return Response({'status': 'success', 'message': 'Payment verified successfully'})
#         else:
#             return Response({'status': 'failed', 'message': 'Payment verification failed'})
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
