from msilib import CreateRecord
from multiprocessing import AuthenticationError
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from account.models import Account
from django.core.validators import MinValueValidator
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Note(models.Model):
    title               = models.CharField(max_length=60) 
    creator             = models.ForeignKey(Account,on_delete=models.CASCADE)
    price               = models.IntegerField(validators=[MinValueValidator(0)])
    category            = models.ForeignKey(Category,on_delete=models.CASCADE)
    date_created        = models.DateTimeField(auto_now_add = True)
    last_edit           = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    Note             = models.ForeignKey(Note, on_delete=models.CASCADE)
    comment          =  models.CharField(max_length=300)

    def __str__(self):
        return self.comment