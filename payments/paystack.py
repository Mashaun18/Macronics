import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Paystack:
    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = 'https://api.paystack.co'

    def verify_payment(self, ref, amount=None):
        """Verify a payment using its reference."""
        url = f'{self.BASE_URL}/transaction/verify/{ref}'
        headers = {
            'Authorization': f'Bearer {self.SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.get(url, headers=headers)
            response_data = response.json()

            # Log the Paystack response for debugging
            logger.info("Paystack Response Data: %s", response_data)

            # Check if the response is valid and has a 'data' field
            if response.status_code == 200 and 'data' in response_data:
                if response_data['data']['status'] == 'success':
                    if amount is not None and response_data['data']['amount'] == amount:
                        return response_data
                    return response_data
                else:
                    logger.warning("Payment verification failed: %s", response_data.get('message', 'Unknown error'))
            else:
                logger.error("Invalid response from Paystack: %s", response_data)
                return None

        except requests.exceptions.RequestException as e:
            logger.error("Request to Paystack failed: %s", str(e))
            return None
        except ValueError as ve:
            logger.error("Error decoding JSON response: %s", str(ve))
            return None
        except Exception as e:
            logger.error("An unexpected error occurred: %s", str(e))
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