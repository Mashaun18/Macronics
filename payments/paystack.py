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
            logger.info("Raw Paystack Response: %s (type: %s)", response.text, type(response.text))

            if response.ok:  # Check if the response status is OK (200)
                response_data = response.json()  # Convert response to JSON
                logger.info("Paystack Response Data: %s (type: %s)", response_data, type(response_data))

                # Ensure response_data is a dictionary and check status
                if isinstance(response_data, dict):
                    if response_data.get('status'):  # If verification was successful
                        # Compare the amount as integers
                        if amount and int(amount) == response_data['data']['amount']:
                            return response_data  # Return the full data on success
                        return {'status': False, 'message': 'Amount does not match.'}  # Return an error if amounts don't match
                    else:
                        logger.error("Verification failed: %s", response_data.get('message', 'Unknown error'))
                        return {'status': False, 'message': response_data.get('message', 'Verification failed')}  # Return an error dict
                else:
                    logger.error("Invalid response structure: %s", response_data)
                    return {'status': False, 'message': 'Invalid response structure'}  # Return error for invalid structure
            else:
                logger.error("Invalid response from Paystack: %s", response.json())
                return {'status': False, 'message': 'Invalid response from Paystack'}  # Return error for non-200 response

        except ValueError as ve:
            logger.error("Error decoding JSON response: %s", str(ve))
            return {'status': False, 'message': 'Error decoding JSON response'}  # Return error for JSON decoding issues

        except Exception as e:
            logger.error("An error occurred: %s", str(e))
            return {'status': False, 'message': 'An error occurred during verification'}  # Return error for general exceptions













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