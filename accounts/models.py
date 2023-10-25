from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=11)
    address = models.TextField(max_length=500)
    postal_code = models.CharField(max_length=100)

    def __str__(self):
        return self.user.phone_number


class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name='your name')
    email = models.EmailField(max_length=100, verbose_name='your email')
    phone = models.CharField(max_length=11, verbose_name='your phone')
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'contact us'
        verbose_name_plural = 'contact us'

    def __str__(self):
        return self.name
