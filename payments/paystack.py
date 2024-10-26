import requests
from django.conf import settings
import logging
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

class Paystack:
    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = 'https://api.paystack.co'
    
    def verify_payment(self, reference, amount):
        # Make the request to Paystack
        url = f"{self.BASE_URL}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.SECRET_KEY}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            
            payment_data = response.json()

            if payment_data['status']:
                # Extract necessary information
                transaction_data = payment_data['data']

                # Access properties directly
                transaction_amount = transaction_data['amount']

                # Verify the amount if necessary
                if transaction_amount == int(amount):
                    return {
                        'status': 'success',
                        'message': 'Payment verified successfully',
                        'data': transaction_data
                    }
                else:
                    return {'status': 'error', 'message': 'Amount mismatch'}

            return {'status': 'error', 'message': payment_data['message']}

        except requests.exceptions.RequestException as e:
            logger.error(f"Request to Paystack failed: {str(e)}")
            return {'status': 'error', 'message': 'Failed to reach Paystack API.'}

        except json.JSONDecodeError:
            logger.error("Error decoding JSON response")
            return {'status': 'error', 'message': 'Invalid response from Paystack'}
        
        except Exception as e:
            logger.error(f"Error during payment verification: {str(e)}")
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