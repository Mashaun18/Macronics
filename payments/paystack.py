import requests
from django.conf import settings
import logging
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

class Paystack:
    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = 'https://api.paystack.co'

    # Method to initialize the payment
    def initialize_payment(self, email, amount, order_id, reference):
        url = f"{self.BASE_URL}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "amount": amount * 100,  # Convert amount to kobo
            "reference": reference,  # Include reference in the data
            "metadata": {
                "order_id": order_id
            },
            'callback_url': 'https://macronics.onrender.com/api/payments/callback/'
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            logger.debug(f"Paystack response: {response.json()}")
            response.raise_for_status()  # Raises an exception for 4xx/5xx errors
            
            payment_response = response.json()
            if payment_response['status']:
                return {
                    'status': 'success',
                    'authorization_url': payment_response['data']['authorization_url']
                }
            else:
                logger.error(f"Error initializing payment: {payment_response['message']}")
                return {'status': 'error', 'message': payment_response['message']}
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {str(http_err)}")
            return {'status': 'error', 'message': 'Payment initialization failed due to a server error.'}
        except Exception as e:
            logger.error(f"Error initializing payment: {str(e)}")
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