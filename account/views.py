from django.shortcuts import render,redirect
from account.forms import SignUpForm
from django.contrib.auth import login,authenticate

def loginview(request):
    context = {}
    return render(request,'account/login.html',context)

def signupview(request):

    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password = raw_password)
            login(request,account)
            return redirect('home')
        else:
            context['signup_form'] = form
    else:
        form = SignUpForm()
        context['signup_form'] = form
    return render(request,'account/signup.html',context)
