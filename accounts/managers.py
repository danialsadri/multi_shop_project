from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have an phone_number")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
