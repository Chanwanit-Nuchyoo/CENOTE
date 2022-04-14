from django.shortcuts import redirect, render
from base.forms import NoteForm
from base.models import Images,Note
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

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

def addnote(request):
    context = {}
    if request.method == "POST":
        formA = NoteForm(request.POST,request.FILES)
        images = request.FILES.getlist('images')
        if formA.is_valid():
            print('Hello')
            formA.user = request.user
            note_instance = formA.save()
            for f in images:
                image = Images.objects.create(note_instance,f)
                image.save()
                redirect('addnote')

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