from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyUserManager(BaseUserManager):
    def create_user(self, username, email,fullname, password =None):
        if not username:
            raise ValueError("Username Required!")
        if not email:
            raise ValueError("Email Required!")

        user = self.model(
            email = self.normalize_email(email),
            username= username,
            fullname=fullname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,fullname,email, password):
        user = self.create_user(
            username=username,
            fullname=fullname,
            password=password,
            email=self.normalize_email(email),
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
            
            


class User(AbstractBaseUser):

    username = models.CharField(max_length=100,unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254,unique=True)
    # password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    date_join = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','fullname']

    objects= MyUserManager()
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created = False, **kwargs):
    if created:
        Token.objects.create(user=instance)
