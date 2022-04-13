from ast import BinOp
import telnetlib
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.forms import BooleanField, CharField

# create a new user
# create a superuser

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Email is require.")
        if not username:
            raise ValueError("Username is require.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return f'profile_image/{str(self.pk)}/{"profile_image.png"}'

def get_default_profile_image():
    return "account/default.png"

class Account(AbstractBaseUser):

    ############# Require Fields from AbstractBaseUser ##################################
    email               = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username            = models.CharField(max_length=10, unique = True)
    date_joined         = models.DateTimeField(verbose_name='date joined', auto_now_add = True)
    last_login          = models.DateTimeField(verbose_name='last login', auto_now = True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    ######################################################################################
    profile_image       = models.ImageField(max_length=255,upload_to=get_profile_image_filepath,null=True, blank = True, default=get_default_profile_image)
    hide_email          = models.BooleanField(default=True)
    bio                 = models.TextField(max_length=300,null=True, blank=True,default='-')

    objects = MyAccountManager()

    ################ Change to using email for login instead of username #################
    USERNAME_FIELD      = 'email'
    ######################################################################################

    REQUIRED_FIELDS       = ['username']
    
    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/(self.pk)/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True