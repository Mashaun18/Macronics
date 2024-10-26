import requests
from django.conf import settings
import logging
from django.http import JsonResponse
import json  # Don't forget to import json

logger = logging.getLogger(__name__)

class Paystack:
    SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    BASE_URL = 'https://api.paystack.co'

    @staticmethod
    def verify_payment(request):
        reference = request.GET.get('reference')
        amount = request.GET.get('amount')

        # Make the request to Paystack
        url = f"{Paystack.BASE_URL}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {Paystack.SECRET_KEY}"  # Use the secret key from settings
        }

        response = requests.get(url, headers=headers)

        try:
            # Make sure to parse the response correctly
            payment_data = response.json()

            if payment_data['status']:
                # Extract necessary information
                transaction_data = payment_data['data']

                # You can now access properties directly
                transaction_id = transaction_data['id']
                transaction_amount = transaction_data['amount']
                transaction_status = transaction_data['status']

                # Verify the amount if necessary
                if transaction_amount == int(amount):
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Payment verified successfully',
                        'data': transaction_data
                    })
                else:
                    return JsonResponse({'status': 'error', 'message': 'Amount mismatch'}, status=400)

            return JsonResponse({'status': 'error', 'message': payment_data['message']}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid response from Paystack'}, status=400)
        except Exception as e:
            logger.error(f"Error during payment verification: {str(e)}")  # Log the error
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)














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