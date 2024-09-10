from django.shortcuts import render
from rest_framework import viewsets, status, filters, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions 
    (GET, POST, PUT, DELETE) for the Product model.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = pagination.PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        """Handles GET request for a list of products."""
        products = self.queryset.all()
        serializer = self.serializer_class(products, many=True)
        return Response({"products": serializer.data, "message": "Products retrieved successfully"}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handles GET request for a single product by ID."""
        try:
            product = self.queryset.get(pk=pk)
            serializer = self.serializer_class(product)
            return Response({"product": serializer.data, "message": "Product retrieved successfully"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handles POST request to create a new product."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handles PUT request to update an existing product."""
        try:
            product = self.queryset.get(pk=pk)
            serializer = self.serializer_class(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handles DELETE request to delete a product."""
        try:
            product = self.queryset.get(pk=pk)
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)