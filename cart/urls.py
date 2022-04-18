from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    
    path('cart/',views.cart_view,name='cart_view') ,
    path('cart/add/<int:id>/<int:quantity>/',views.add_item_to_cart_view,name="add_item_to_cart_view"),
    path('cart/add/<int:id>/',views.add_item_to_cart_view,name="add_item_to_cart_view"),
    path('cart/remove/<int:id>/<int:quantity>/',views.remove_item_from_cart_view,name="remove_item_from_cart_view"),
    path('cart/remove/<int:id>/',views.remove_item_from_cart_view,name="remove_item_from_cart_view"),
    path('cart/clear/',views.clear_item_in_cart_view,name="clear_item_in_cart_view"),


    
]
               