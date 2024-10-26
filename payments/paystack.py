import requests
from django.conf import settings
import logging
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

class Paystack:
    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = 'https://api.paystack.co'
    
    def verify_payment(self, reference):
        # Make the request to Paystack
        url = f"{Paystack.BASE_URL}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {Paystack.SECRET_KEY}"
        }

        response = requests.get(url, headers=headers)
        try:
            payment_data = response.json()
            return payment_data
        except json.JSONDecodeError:
            logger.error("JSON decode error from Paystack response.")
            return {'status': 'error', 'message': 'Invalid response from Paystack'}
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