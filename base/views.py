from unicodedata import category
from django.shortcuts import redirect, render
from account.models import Account
from base.forms import NoteForm
from base.models import Images,Note
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Note

def home(request):
    context = {}
    return render(request,'base/index.html',context)

def open(request):
    context = {}
    return render(request, 'base/open.html',context)

def preview(request):
    notes = Note.objects.all()
    context = {
        'notes':notes
    }
    return render(request, 'base/previewnote.html',context)

def book(request):
    notes = Note.objects.all()

    context = {
        'notes':notes
    }
    return render(request,'base/book.html',context)

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
            note.pdf_file = formA.cleaned_data.get('pdf_file')
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


def note_view(request,slug):
    note = get_object_or_404(Note,slug=slug)
    context = {
        'note':note,
    }
    # รอ html สำหรับหน้า Note Detail
    return render(request,'.html',context)