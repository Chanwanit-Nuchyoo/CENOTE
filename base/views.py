from multiprocessing import context
from unicodedata import category
from django.shortcuts import redirect, render
from django.urls import reverse
from account.models import Account
from base.forms import NoteForm,NoteEditForm,CommentForm
from base.models import Images,Note,Comment
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category, Note
from django.views.generic import ListView
from django.shortcuts import render
from django.db.models import Count
from django.apps import apps


def home(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    return render(request,'base/index.html',context)

def open(request):
    context = {}
    return render(request, 'base/open.html',context)

def book(request):
    notes = Note.objects.all()
    notes = notes.order_by('-date_created')
    rank=[]
    search = ''
    for i in notes:
        rank.append(i)
    
    if request.method == 'POST':
        if request.POST.get('search'):
            search = request.POST.get('search')
            notes = Note.objects.filter(title__icontains=search)

    #sort rank ลองใช้order_byแล้วไม่เวิร์ค
    for i in range(len(rank)-1):
    # range(n) also work but outer loop will
    # repeat one time more than needed.
 
        # Last i elements are already in place
        for j in range(0,len(rank)-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if rank[j].likes.count() > rank[j + 1].likes.count() :
                rank[j], rank[j + 1] = rank[j + 1], rank[j]
    if len(rank) == 0:
        rank1 = None
        rank2 = None
        rank3 = None
    elif len(rank) == 1:
        rank.reverse()
        rank1 = rank[0]
        rank2 = None
        rank3 = None
    elif len(rank) == 2:
        rank.reverse()
        rank1 = rank[0]
        rank2 = rank[1]
        rank3 = None
    else:
        rank.reverse()
        rank1 = rank[0]
        rank2 = rank[1]
        rank3 = rank[2]
    # Category ID 
    # 1 = Hardware
    # 2 = NETWORK
    # 3 = Software
    categories = Category.objects.all()
    cate = request.session.get('category') or 0
    if cate:
        notes = notes.filter(category_id=cate)

    category_verbose = {
        '0':'All',
        '1':'Hardware',
        '2':'Network',
        '3':'Software',
    }

    
    order_id = request.session.get('order') or 0
    if order_id == 0:
        notes = notes.order_by('-date_created')
    elif order_id == 1:
        notes = notes.order_by('-view_count')
    elif order_id == 2:
        notes = notes.annotate(like_count=Count('likes')).order_by('-like_count')

    paginator = Paginator(notes, per_page=8)
    page_num = request.GET.get('page') or 1
    page_object = paginator.get_page(page_num)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page_num,on_each_side=1)


    context = {
        'notes':notes,
        'count':paginator.count,
        'page_object':page_object,
        #'note_paginator':note_paginator,
        'page_num':int(page_num),
        'rank1': rank1,
        'rank2': rank2,
        'rank3': rank3,
        'categories':categories,
        'categ_id':cate,
        'order_id':order_id,
        'category_verbose':category_verbose.get(str(cate)),
        }
    #print(rank)
    return render(request,'base/book.html',context)

def default_cover():
    return 'account/{filename}{randomint}{ext}'.format(filename='defaultcover' , randomint=random.randint(1,7) ,ext='.jpg')

@login_required(login_url='/login')
def addnote(request):
    context = {}
    if request.method == "POST":
        formA = NoteForm(request.POST,request.FILES)
        images = request.FILES.getlist('images')
        if formA.is_valid():
            
            note = Note()
            note.user = request.user
            note.title = formA.cleaned_data.get('title')
            note.info = formA.cleaned_data.get('info')
            note.price = formA.cleaned_data.get('price')
            note.category = formA.cleaned_data.get('category')
            note.pdf_file = request.FILES.get('pdf')
            if request.FILES.get('cover'):
                note.cover = request.FILES.get('cover')
            else:
                note.cover = default_cover()
            note.save()
            if images:
                for f in images:
                    #print(f)
                    image = Images()
                    image.note = Note.objects.get(id=note.pk)
                    image.image = f
                    image.save()
            context['formA'] = NoteForm()
            # return r edirect('home')
            return redirect(reverse('note_view', kwargs={"id": note.id}))

        else:
            context['formA'] = formA
    else:
        formA = NoteForm()
        context['formA'] = formA
    return render(request,'base/addnote.html',context)

@login_required(login_url='/login')
def note_edit_view(request,id):
    
    # User can edit the note if it is their owns.
    # Admins have all privilege to edit every notes.
    user = request.user
    note = get_object_or_404(Note,pk=id)
    note_owner = note.user

    if request.user.id != note.user.id:
        return redirect(reverse('profile'))

    # Populate the fields
    form = NoteEditForm(instance=note)
    
    if request.method == "POST":
        form = NoteEditForm(request.POST,request.FILES,instance=note)
        if form.is_valid():
            form.save()
            #print('/editnote:Form saved')
            images = request.FILES.getlist('images')

            if request.FILES.get('cover'):
                note.cover = request.FILES.get('cover')
                note.save()

            if images:
                #print("/editnote: priview images update.")
                # Remove all old preview images
                Images.objects.filter(note=note).delete()
                # Replace with new images
                for f in images:
                    image = Images()
                    image.note = Note.objects.get(id=note.pk)
                    image.image = f
                    image.save()
            messages.success(request,'Note updated')
            
    images =[image.image.url for image in Images.objects.filter(note=note)]

    context = {
        'formA':form,
        'note' :note,
        'preview_images':images,
    }


    return render(request,'base/editnote.html',context)

def note_view(request,id):
    note = get_object_or_404(Note,id=id)
    note.view_count = note.view_count+1
    comment_form = CommentForm()
    note.save()
    author = get_object_or_404(Account,id=note.user.id)
    author.view_count += 1
    author.save()

    try :
        has_brought = request.user.shelf.has_brought(note)
    except Exception:
        has_brought = False

    if request.method=='POST':

        # Check if user is authenticated before comment
        if not request.user.is_authenticated:
            return redirect(reverse('loginview'))

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.note = note
            comment.commenter = request.user
            comment.save()
            comment_form = CommentForm()
            note.comment_count += 1
            note.save()
            return redirect('note_view', id = id)
        else:
            comment_form = CommentForm()
            print('invalid form')

    category_verbose = {
        '0':'All',
        '1':'Hardware',
        '2':'Network',
        '3':'Software',
    }

    comments = Comment.objects.filter(note = id)
    images = Images.objects.filter(note=id)
    context = {
        'note':note,
        'images':images,
        'comment_form':comment_form,
        'comments':comments,
        'has_brought': has_brought,
        'category_verbose': category_verbose.get(str(note.category.pk)),
    }
    return render(request,'base/noteview.html',context)

def cateview(request,cate):
    request.session['category'] = cate
    request.session['order'] = 0
    
    return redirect('book')

def all(request):
    request.session['category'] = None
    return redirect('book')

@login_required(login_url='/login')
def like1(request,noteid):
    note = get_object_or_404(Note,id=noteid)
    author = get_object_or_404(Account,id=note.user.id)
    user = note.likes.all()
    user = user.filter(id=request.user.id)
    if user:
        note.likes.remove(request.user)
        author.like_count -= 1
        author.save()
    else:
        note.likes.add(request.user)
        author.like_count += 1
        author.save()
    note.save()
    return redirect('book')

@login_required(login_url='/login')
def like2(request,noteid):
    note = get_object_or_404(Note,id=noteid)
    author = get_object_or_404(Account,id=note.user.id)
    user = note.likes.all()
    user = user.filter(id=request.user.id)
    if user:
        note.likes.remove(request.user)
        author.like_count -= 1
        author.save()
    else:
        note.likes.add(request.user)
        author.like_count += 1
        author.save()
    note.save()
    return redirect('profile')

@login_required(login_url='/login')
def like3(request,noteid):
    note = get_object_or_404(Note,id=noteid)
    author = get_object_or_404(Account,id=note.user.id)
    user = note.likes.all()
    user = user.filter(id=request.user.id)
    if user:
        note.likes.remove(request.user)
        author.like_count -= 1
        author.save()
    else:
        note.likes.add(request.user)
        author.like_count += 1
        author.save()
    note.save()
    return redirect('note_view', id = noteid)

@login_required(login_url='/login')
def payment(request):
    if request.method == 'POST':
        # GET CREDIT CARD INFOMATION HERE        
        
        # Checkout Cart
        user = request.user
        user.cart.checkout()

        return redirect(reverse('paymentconfirm'))

    context = {}
    return render(request,'base/payment.html',context)

@login_required(login_url='/login')
def paymentconfirm(request):
    context = {}
    request.user.cart.remove_all_item()
    return render(request,'base/paymentconfirm.html',context)

@login_required(login_url='/login')
def order_history_view(request):
    Shelf = apps.get_model('base','Shelf')
    ShelfItem = apps.get_model('base','ShelfItem')
    shelf = Shelf.objects.get_or_create(account=request.user)
    shelfitems = ShelfItem.objects.all().filter(shelf__account=request.user)
    context = {
        'shelf':shelf,
        'items':shelfitems,
    }
    return render(request,'account/orderhistory.html',context)

def sort(request,s):
    request.session['order'] = s
    return redirect('book')
