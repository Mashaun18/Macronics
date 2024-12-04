from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from customers.models import UserRole
from .models import Vendor
from .serializers import VendorSerializer
from payments.paystack import Paystack  # Assuming you have a Paystack helper file

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == UserRole.VENDOR:
            return Vendor.objects.filter(user=user)
        return Vendor.objects.all()
    
    def create(self, request, *args, **kwargs):
        vendor = Vendor.objects.get(user=request.user)
        if not vendor.is_subscription_active():
            return Response(
                {"error": "You must pay the listing fee to access this feature."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def pay_listing_fee(self, request):
        """
        Handles payment for vendor listing fee.
        """
        user = request.user

        # Ensure the user is a vendor
        if user.user_type != UserRole.VENDOR:
            return Response({'error': 'Only vendors can pay the listing fee.'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the vendor has already paid
        vendor = get_object_or_404(Vendor, user=user)
        if vendor.listing_fee_paid:
            return Response({'message': 'You have already paid the listing fee.'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the payment using Paystack
        paystack = Paystack()
        amount = 2000 * 100  # Paystack requires amounts in kobo
        email = user.email
        reference = paystack.generate_reference()

        try:
            payment_url = paystack.initialize_payment(email=email, amount=amount, reference=reference, metadata={'vendor_id': vendor.id})
            return Response({'message': 'Payment initiated successfully.', 'payment_url': payment_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error initiating payment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def verify_payment(self, request):
        """
        Verifies the payment for the vendor listing fee.
        """
        reference = request.GET.get('reference')
        if not reference:
            return Response({'error': 'No reference provided'}, status=status.HTTP_400_BAD_REQUEST)

        paystack = Paystack()

        try:
            payment_data = paystack.verify_payment(reference)
            if payment_data.get('status') and payment_data['data']['status'] == 'success':
                data = payment_data['data']
                metadata = data.get('metadata', {})
                vendor_id = metadata.get('vendor_id')

                if not vendor_id:
                    return Response({'error': 'Vendor ID not found in payment metadata.'}, status=status.HTTP_400_BAD_REQUEST)

                vendor = get_object_or_404(Vendor, id=vendor_id)

                if vendor.listing_fee_paid:
                    return Response({'message': 'Payment already verified.'}, status=status.HTTP_200_OK)

                # Mark vendor as having paid the listing fee
                vendor.listing_fee_paid = True
                vendor.save()

                return Response({'message': 'Payment verified and listing fee updated.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment verification failed.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'Error verifying payment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class VendorViewSet(viewsets.ModelViewSet):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.user_type == UserRole.VENDOR:
#             return Vendor.objects.filter(user=user)
#         return Vendor.objects.all()