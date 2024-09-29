from django.shortcuts import render
from rest_framework import viewsets, status, filters, pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer

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

    def retrieve(self, request, identifier=None):
        """Handles GET request for a single product by ID, name, or slug."""
        try:
            # Check if identifier is an integer (ID)
            if identifier.isdigit():
                product = self.queryset.get(pk=int(identifier))
            else:
                # Check if the identifier is a slug or name
                product = self.queryset.filter(slug=identifier).first()
                if not product:  # If not found by slug, try by name
                    product = self.queryset.filter(name=identifier).first()

            if product:
                serializer = self.serializer_class(product)
                return Response({"product": serializer.data, "message": "Product retrieved successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handles POST request to create a new product."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, identifier=None):
        """Handles PUT request to update an existing product."""
        try:
            # Retrieve product based on identifier
            if identifier.isdigit():
                product = self.queryset.get(pk=int(identifier))
            else:
                product = self.queryset.filter(slug=identifier).first()
                if not product:
                    product = self.queryset.filter(name=identifier).first()

            if product:
                serializer = self.serializer_class(product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, identifier=None):
        """Handles DELETE request to delete a product."""
        try:
            # Retrieve product based on identifier
            if identifier.isdigit():
                product = self.queryset.get(pk=int(identifier))
            else:
                product = self.queryset.filter(slug=identifier).first()
                if not product:
                    product = self.queryset.filter(name=identifier).first()

            if product:
                product.delete()
                return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
