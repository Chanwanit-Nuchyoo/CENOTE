from django.shortcuts import render

def loginview(request):
    context = {}
    return render(request,'account/login.html',context)

def signupview(request):
    context = {}
    return render(request,'account/signup.html',context)
