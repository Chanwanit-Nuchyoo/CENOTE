from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):
    context = {}
    return render(request,'base/index.html',context)

def open(request):
    context = {}
    return render(request, 'base/open.html',context)

def book(request):
    context = {}
    return render(request,'base/book.html',context)
