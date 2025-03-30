from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """مدیریت کاربران با شماره موبایل به جای نام کاربری"""
    def create_user(self, phone, password=None, role='customer', **extra_fields):
        """ایجاد یوزر عادی"""
        if not phone:
            raise ValueError('شماره موبایل الزامی است!')
        extra_fields.setdefault('role', role)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """ایجاد سوپریوزر"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('must be True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('must be True')

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """مدل کاربر با شماره موبایل و نقش های متفاوت"""
    ROLE_CHOISES = (
        ('admin',"مدیر"),
        ('seller',"فروشنده"),
        ('customer',"مشتری"),
    )
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    address = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_CHOISES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['last_name']

    def __str__(self):
        return f"{self.phone} - {self.get_role_display()}"

