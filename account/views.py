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
from account.forms import AccountEditForm
from django.db.models import Count

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

@login_required(login_url='/login/')
def edit_profile_view(request):
    # account = get_object_or_404(Account,id=request.user.id)
    # if request.method == 'POST':
    #     print(request.FILES)
    #     if request.FILES:
    #         account.profile_image = request.FILES.get('profilePic')
    #     if request.POST.get('name'):
    #         account.name = request.POST.get('name')
    #     if request.POST.get('info'):
    #         account.info = request.POST.get('info')
    #     if request.POST.get('github'):
    #         print('Ihatethisproject')
    #         account.github = request.POST.get('github')
    #     if request.POST.get('contact_email'):
    #         account.contact_email = request.POST.get('contact_email')
    #     if request.POST.get('youtube'):
    #         account.youtube = request.POST.get('youtube')
    #     account.save()
    #     return redirect('profile')
    
    # context = {
    # }
    form = AccountEditForm(instance=request.user)

    if request.method == 'POST':
        form = AccountEditForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile',username=request.user.username)
        else:
            print("FORM IS NOT VALID")
            

    context = {
        'form':form,
    }
    
    return render(request,'account/editprofile.html',context)
    
    
    # return render(request,'account/editprofile.html',context)

@login_required(login_url='/login')
def profile(request,username):
    user = get_object_or_404(Account, username=username)
    if not user:
        return redirect('home')
    notes = Note.objects.filter(user=user.id)
    profilesort = request.session.get('profilesort') or 0
    if profilesort == 0:
        notes = notes.order_by('-date_created')
    elif profilesort == 1:
        notes = notes.order_by('-view_count')
    elif profilesort == 2:
        notes = notes.annotate(like_count=Count('likes')).order_by('-like_count')
    context = {
        'notes':notes,
        'profilesort': profilesort,
        'user':user,
    }
    return render(request, 'account/profile.html',context)

@login_required(login_url='/login')
def profilesort(request,sortid,username):
    request.session['profilesort'] = sortid
    return redirect('profile', username=username)