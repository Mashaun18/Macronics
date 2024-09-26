from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserSignupView, user_profile, user_dashboard

router = DefaultRouter()
router.register(r'customers', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('profile/', user_profile, name='user_profile'),
    path('dashboard/', user_dashboard, name='user_dashboard'),  # Already added
]
