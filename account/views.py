from django.shortcuts import render, redirect
from account.forms import SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib import messages
from account.models import Account
from account.backends import CaseInsensitiveModelBackend
from django.contrib.auth.decorators import login_required
from base.models import Note
from django.shortcuts import get_object_or_404

def loginview(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
        except:
            # messages.error(request, 'User does not exist.')
            messages.error(request, 'Incorrect username or password')
            return redirect(reverse('loginview'))
            
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password')
            return redirect(reverse('loginview'))
    return render(request, 'account/login.html', context)



def signupview(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['signup_form'] = form
    else:
        form = SignUpForm()
        context['signup_form'] = form
    return render(request, 'account/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')

def edit_profile_view(request):
    account = get_object_or_404(Account,id=request.user.id)
    if request.method == 'POST':
        print(request.FILES)
        if request.FILES:
            account.profile_image = request.FILES.get('profilePic')
        if request.POST.get('name'):
            account.name = request.POST.get('name')
        if request.POST.get('info'):
            account.info = request.POST.get('info')
        if request.POST.get('github'):
            account.github = request.POST.get('github')
        if request.POST.get('contact_email'):
            account.contact_email = request.POST.get('contact_email')
        if request.POST.get('youtube'):
            account.youtube = request.POST.get('youtube')
        account.save()
    
    context = {
    }
    return render(request,'account/editprofile.html',context)

def profile(request):
    notes = Note.objects.filter(user=request.user.id)
    context = {
        'notes':notes,
    }
    return render(request, 'account/profile.html',context)

