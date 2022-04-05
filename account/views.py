from django.shortcuts import render,redirect
from account.forms import SignUpForm, SigninForm
from django.contrib.auth import login,authenticate,logout

def loginview(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = SigninForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = SigninForm()

    context['form'] = form
    return render(request, 'account/login.html', context)

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

def logout_view(request):
    logout(request)
    return redirect('home')
