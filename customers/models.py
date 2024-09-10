from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class UserRole(models.TextChoices):
    ADMIN = 'admin', 'admin'
    VENDOR = 'vendor', 'vendor'
    CUSTOMER = 'customer', 'customer'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None, user_type=None):
        if not email:
            raise ValueError('Users must have an email address')
        if user_type not in [role.value for role in UserRole]:
            raise ValueError('Invalid user type')
        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.user_type = user_type
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, first_name='', last_name=''):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=UserRole.ADMIN
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Userr(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=255, unique=True)
    user_type = models.CharField(max_length=50, choices=[(role.value, role.name) for role in UserRole])
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=100, default='Not specified')
    city = models.CharField(max_length=100, default='Not specified')
    state = models.CharField(max_length=100, default='Not specified')
    country = models.CharField(max_length=100, default='Nigeria')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.email
