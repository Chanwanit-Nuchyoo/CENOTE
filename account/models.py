from ast import BinOp
from email.policy import default
import telnetlib
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.forms import BooleanField, CharField
from django.db.models.signals import post_save

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

        # from cart.models import Cart        
        # Cart.objects.create(account=user)

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
    ############# Profile Info ##########################################################
    profile_image       = models.ImageField(max_length=255,upload_to=get_profile_image_filepath,null=True, blank = True, default=get_default_profile_image)
    hide_email          = models.BooleanField(default=True)
    like_count          = models.IntegerField(default=0, null=True, blank=True)
    view_count          = models.IntegerField(default=0, null=True, blank=True)
    name                = models.CharField(max_length=50,null=True,blank=True)
    info                = models.TextField(max_length=300,null=True, blank=True,default='-')
    github              = models.CharField(max_length=50,null=True,blank=True)
    contact_email       = models.CharField(max_length=50,null=True,blank=True)
    youtube             = models.CharField(max_length=60,null=True,blank=True)

    objects = MyAccountManager()

    ################ Change to using email for login instead of username #################
    USERNAME_FIELD      = 'email'
    ######################################################################################

    REQUIRED_FIELDS       = ['username']
    
    def __str__(self):
        return self.username

    def get_cart_url(self):
        from django.urls import reverse
        return reverse('cart:cart')

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/(self.pk)/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
        
        

        # from cart.models import Cart
        # cart = Cart(account=user)
        # print('saving cart')
        # cart.save()
def create_cart_for_account(sender,instance,*args,**kwargs):
    from cart.models import Cart        
    print(sender)
    
    try:
        instance.cart    
    except Exception:
        cart = Cart(account=instance)
        cart.save()
        print("saving cart")
    return 

post_save.connect(create_cart_for_account,sender=Account)