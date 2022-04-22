from multiprocessing import context
from unicodedata import category
from django.shortcuts import redirect, render
from django.urls import reverse
from account.models import Account
from base.forms import NoteForm,NoteEditForm
from base.models import Images,Note
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import random
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Category, Note
from django.views.generic import ListView
from django.shortcuts import render


def home(request):
    context = {}
    return render(request,'base/index.html',context)

def open(request):
    context = {}
    return render(request, 'base/open.html',context)

def book(request):
    notes = Note.objects.all()
    rank=[]
    for i in notes:
        rank.append(i)
    
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
    note_paginator = Paginator(notes,2)#parameter คือจำนวนโน๊ตที่มีใน 1 page
    page_num = request.GET.get('page',1)
    page = note_paginator.get_page(page_num) 

    cate = request.session.get('category') or 0
    if cate:
        notes = notes.filter(category__name__contains=cate)
    context = {
        'notes':notes,
        'count':note_paginator.count,
        'page':page,
        'note_paginator':note_paginator,
        'page_num':int(page_num),
        'rank1': rank1,
        'rank2': rank2,
        'rank3': rank3,
        }
    print(rank)
    return render(request,'base/book.html',context)

def default_cover():
    return 'account/{filename}{randomint}{ext}'.format(filename='defaultcover' , randomint=random.randint(1,7) ,ext='.jpg')

# @login_required(login_url='/login')
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
                    print(f)
                    image = Images()
                    image.note = Note.objects.get(id=note.pk)
                    image.image = f
                    image.save()
            context['formA'] = NoteForm()
            return redirect('home')

        else:
            context['formA'] = formA
    else:
        formA = NoteForm()
        context['formA'] = formA
    return render(request,'base/addnote.html',context)

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
            print('/editnote:Form saved')
            images = request.FILES.getlist('images')

            if request.FILES.get('cover'):
                note.cover = request.FILES.get('cover')
                note.save()

            if images:
                print("/editnote: priview images update.")
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
    note.save()
    author = get_object_or_404(Account,id=note.user.id)
    author.view_count += 1
    author.save()
    images = Images.objects.filter(note=id)
    context = {
        'note':note,
        'images':images,
    }
    # รอ html สำหรับหน้า Note Detail
    return render(request,'base/noteview.html',context)

def cateview(request,cate):
    request.session['category'] = cate
    return redirect('book')

def all(request):
    request.session['category'] = None
    return redirect('book')

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

def payment(request):
    context = {}
    return render(request,'base/payment.html',context)
