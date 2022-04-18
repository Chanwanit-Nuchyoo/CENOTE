from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from .models import Cart,Item
from base.models import Note


@login_required(login_url='/login/')
def cart_view(request):
    
    cart = request.user.cart 
    context = {
        'cart':cart,
    }
    return render(request,'cart/cart_view.html',context)

@login_required
def add_item_to_cart_view(request,id,quantity=1):
    user = request.user
    note = get_object_or_404(Note,pk=id)
    user.cart.add_item(note=note,quantity=quantity) 
    return redirect(reverse('note_view',kwargs={'id':note.id}))
    
@login_required
def remove_item_from_cart_view(request,id,quantity=1):
    user = request.user
    note = get_object_or_404(Note,pk=id)
    if user.cart.items.filter(note=note).exists():
        user.cart.remove_item(note=note,quantity=quantity) 
    return redirect(reverse('note_view',kwargs={'id':note.id}))

@login_required
def clear_item_in_cart_view(request):
    user = request.user
    if user.cart.items:
        user.cart.items.all().delete()

    return redirect(reverse('cart:cart_view'))