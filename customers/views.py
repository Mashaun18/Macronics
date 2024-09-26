from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Userr
from .serializers import UserSerializer, UserSignupSerializer
from customers import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from orders.models import Order
from orders.serializers import OrderSerializer
# Create your views here. 



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        
        if user is None:
            raise ValidationError({"detail": "Invalid credentials"})
        if not user.is_active:
            raise ValidationError({"detail": "User account is disabled."})

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.user_type,
            'user': UserSerializer(user).data  # Include user profile data
        }

        return data



class ObtainTokenView(APIView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserSignupView(generics.CreateAPIView):
    queryset = Userr.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
def user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def user_dashboard(request):
    user = request.user
    
    # User Profile
    user_serializer = UserSerializer(user)
    
    # Cart details (assuming "status='cart'" means it's the active cart)
    cart = Order.objects.filter(user=user, status='cart').first()
    cart_serializer = OrderSerializer(cart) if cart else None
    
    # Order history (exclude cart status)
    orders = Order.objects.filter(user=user).exclude(status='cart')
    orders_serializer = OrderSerializer(orders, many=True)

    data = {
        'user_profile': user_serializer.data,
        'cart_details': cart_serializer.data if cart else None,
        'order_history': orders_serializer.data
    }
    
    return Response(data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Userr.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

    def list(self, request):
        """Handles GET request for a list of users."""
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

    def retrieve(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Userr.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
            serializer = self.serializer_class(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Userr.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except Userr.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        