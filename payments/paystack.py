import requests
from django.conf import settings
import logging
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

class Paystack:
    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.base_url = 'https://api.paystack.co'
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def initialize_payment(self, order):
        # Assuming 'order' is an instance of Order
        data = {
            'amount': int(order.total_amount * 100),  # Amount in kobo
            'currency': 'NGN',
            'email': order.user.email,
            'metadata': {
                'order_id': order.id,  # Include the order ID here
                # Add other metadata as needed
            },
            'callback_url': 'https://macronics.onrender.com/api/payments/callback/'  # Optional
        }

        try:
            response = requests.post(f"{self.base_url}/transaction/initialize", json=data, headers=self.headers)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses
            logger.debug(f"Paystack initialization response: {response.json()}")
            return response.json()  # Return the response data as JSON
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred while initializing payment: {str(http_err)}")
            return {'status': 'error', 'message': 'Payment initialization failed due to server error.'}
        except Exception as e:
            logger.error(f"Unexpected error during payment initialization: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    # Method to verify the payment
    def verify_payment(self, reference):
        url = f"{self.BASE_URL}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an exception for 4xx/5xx errors

            payment_data = response.json()
            if payment_data['status'] is True:
                return payment_data
            else:
                logger.error(f"Payment verification failed: {payment_data['message']}")
                return {'status': 'error', 'message': payment_data['message']}
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {str(http_err)}")
            return {'status': 'error', 'message': 'Payment verification failed due to server error.'}
        except json.JSONDecodeError:
            logger.error("JSON decode error from Paystack response.")
            return {'status': 'error', 'message': 'Received an invalid response from Paystack.'}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {'status': 'error', 'message': str(e)}










# import requests
# from django.conf import settings

# class Paystack:
#     SECRET_KEY = settings.PAYSTACK_SECRET_KEY
#     BASE_URL = 'https://api.paystack.co'

#     def verify_payment(self, ref, amount=None):
#         """Verify a payment using its reference."""
#         url = f'{self.BASE_URL}/transaction/verify/{ref}'
#         headers = {
#             'Authorization': f'Bearer {self.SECRET_KEY}',
#             'Content-Type': 'application/json',
#         }
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             response_data = response.json()
#             if response_data['data']['status'] == 'success':
#                 if amount and response_data['data']['amount'] == amount:
#                     return response_data
#                 return response_data
#         return None