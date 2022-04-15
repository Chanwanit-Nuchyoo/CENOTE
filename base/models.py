from distutils.log import info
from email.policy import default
from msilib import CreateRecord
from multiprocessing import AuthenticationError
from trace import CoverageResults
from turtle import ondrag
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from account.models import Account
from django.core.validators import MinValueValidator
import os
from uuid import uuid4
from website.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse
import random
# Create your models here.
def image_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr= ''.join((random.choice(chars)) for x in range(10))
    return 'images/{username}/{basename}{randomstring}{ext}'.format(username= instance.note.user.username, basename= basefilename, randomstring= randomstr, ext= file_extension)

def pdf_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr= ''.join((random.choice(chars)) for x in range(10))
    return 'pdf/{username}/{basename}{randomstring}{ext}'.format(username= instance.user.username, basename= basefilename, randomstring= randomstr, ext= file_extension)

def cover_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr= ''.join((random.choice(chars)) for x in range(10))
    return 'cover/{username}/{basename}{randomstring}{ext}'.format(username= instance.user.username, basename= basefilename, randomstring= randomstr, ext= file_extension)

def default_cover():
    return 'account/{filename}{randomint}{ext}'.format(filename='defaultcover' , randomint=random.randint(1,7) ,ext='.jpg')

class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Note(models.Model):
    title               = models.CharField(max_length=60) 
    info                = models.TextField(max_length=100)
    user                = models.ForeignKey(Account,on_delete=models.CASCADE)
    price               = models.IntegerField(validators=[MinValueValidator(0)])
    category            = models.ForeignKey(Category,on_delete=models.CASCADE)
    cover               = models.ImageField(upload_to=cover_path,blank=True,null=True,default=default_cover)
    pdf_file            = models.FileField(upload_to=pdf_path)
    date_created        = models.DateTimeField(auto_now_add = True)
    last_edit           = models.DateTimeField(auto_now=True)

    # PK for each note.
    slug                = models.SlugField(unique=True,max_length=600,null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("note_view", kwargs={"slug": self.slug})

# Use for generate slug for Note
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator,sender=Note)



class Comment(models.Model):
    note             = models.ForeignKey(Note, on_delete=models.CASCADE)
    comment          =  models.CharField(max_length=300)
    date_created     = models.DateTimeField(auto_now_add=True,null=True)
    commenter        = models.ForeignKey(Account,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

class Images(models.Model):
    note            = models.ForeignKey(Note, on_delete=models.CASCADE,default=None,null=True)
    image           = models.ImageField(upload_to=image_path,null = True ,blank= True )

    def __str__(self):
        return str(self.image.url) or None

