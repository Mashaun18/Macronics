import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Paystack:
    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = 'https://api.paystack.co'

    @classmethod
    def verify_payment(cls, ref, amount=None):
        """Verify a payment using its reference."""
        url = f'{cls.BASE_URL}/transaction/verify/{ref}'
        headers = {
            'Authorization': f'Bearer {cls.SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            if response_data['data']['status'] == 'success':
                if amount and response_data['data']['amount'] != amount:
                    logger.error(f"Amount mismatch: expected {amount}, got {response_data['data']['amount']}")
                    return None
                return response_data
            else:
                logger.error(f"Payment verification failed: {response_data}")
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as e:
            logger.error(f"Error verifying payment: {str(e)}")

        return None






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