from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserSignupView


router = DefaultRouter()
router.register(r'customers', UserViewSet)  # Register the User viewset with the router

urlpatterns = [
    path('', include(router.urls)),  # Include the router's URLs
    path('signup/', UserSignupView.as_view(), name='user-signup'),
]
