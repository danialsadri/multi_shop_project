from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('phone_number'))
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True, verbose_name=_('email'))
    full_name = models.CharField(max_length=100, verbose_name=_('full_name'))
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is_admin'))

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربر ها')

    def __str__(self):
        return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=100, verbose_name=_('token'))
    phone = models.CharField(max_length=11, verbose_name=_('phone_number'))
    code = models.PositiveSmallIntegerField(verbose_name=_('code'))
    expiration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('expiration_date'))

    class Meta:
        verbose_name = _('otp')
        verbose_name_plural = _('otps')

    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('user'))
    full_name = models.CharField(max_length=100, verbose_name=_('full_name'))
    email = models.EmailField(max_length=100, verbose_name=_('email'))
    phone = models.CharField(max_length=11, verbose_name=_('phone_number'))
    address = models.TextField(max_length=500, verbose_name=_('address'))
    postal_code = models.CharField(max_length=100, verbose_name=_('postal_code'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return self.user.phone_number


class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('your name'))
    email = models.EmailField(max_length=100, verbose_name=_('your email'))
    phone = models.CharField(max_length=11, verbose_name=_('your phone'))
    subject = models.CharField(max_length=100, verbose_name=_('subject'))
    message = models.TextField(max_length=500, verbose_name=_('message'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = _('contact us')
        verbose_name_plural = _('contact us')

    def __str__(self):
        return self.name
