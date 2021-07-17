from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# # 1 способ, OneToOneField
# class Profile(models.Model):
#
#     phone = models.CharField(verbose_name='номер телефона', max_length=15, null=False)
#     bio = models.TextField(null=True, blank=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'профиль'
#         verbose_name_plural = 'профили'

# # 2 способ, AbstractUser
# class User(AbstractUser):
#     phone = models.CharField(verbose_name='номер телефона', max_length=15, null=False)
#     bio = models.TextField(null=True, blank=True)
#     photo = models.ImageField(upload_to='users/', verbose_name='фото', null=True, blank=True)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, phone, password):
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password):
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


# 3 способ, AbstractBaseUser
class User(AbstractBaseUser):

    name = models.CharField(verbose_name='имя', max_length=150, null=True, blank=False)
    email = models.EmailField(verbose_name='email', null=False, blank=False, unique=True)
    phone = models.CharField(verbose_name='телефон', max_length=13, null=False, blank=True)
    is_staff = models.BooleanField('staff status', default=False,)
    is_active = models.BooleanField('активен', default=True)
    date_joined = models.DateTimeField('дата регистрации', default=timezone.now)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    objects = CustomUserManager()

    def has_perm(self,  perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser