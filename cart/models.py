from django.db import models
from account.models import Account
from base.models import Note
from django.db.models.signals import post_save
from django.apps import apps


class Cart(models.Model):
    # To get queryset for items in the cart use self.items.all()

    account = models.OneToOneField(Account,on_delete=models.CASCADE,related_name='cart')
    # related_name = ['items',]

    def checkout(self):
        # Checkout entire cart
        # Move notes in cart to owner's shelf
        # Clear all notes in Shelf
        Shelf = apps.get_model('base','Shelf')
        ShelfItem = apps.get_model('base','ShelfItem')
        shelf,created = Shelf.objects.get_or_create(account=self.account)
        
        for item in self.items.all():
            shelfitem = ShelfItem(note=item.note,shelf=shelf)
            shelfitem.save()

        self.remove_all_item()
        
        return shelf


    def total_price(self):
        price = 0        
        price = sum([item.note.price*item.quantity for item in self.items.all()])
        return price

    def total_quantity(self):
        return sum([item.quantity for item in self.items.all()])
    
    def has_brought(self,note):
        Shelf = apps.get_model('base','Shelf')
        shelf = Shelf.objects.get(account=self.account)
        return shelf.has_brought(note)

    def add_item(self,note,quantity=1):
        if self.has_brought(note):
            # User has brought the note, cannot add to the cart
            return 

        if self.items.all().filter(note=note).exists():
            item = self.items.get(note=note)
            
            if item.quantity >= 1:
                return item

            return item.save()
        return self.items.create(cart=self,note=note,quantity=1)

    def remove_item(self,note,quantity=1):
        if self.items.all().filter(note=note).exists():
            item = self.items.get(note=note)
            if item.quantity >= quantity:
                item.quantity -= quantity
                # remove successfully
                if item.quantity == 0:
                    # down to 0
                    return item.delete()
                return item.save()
            else:
                # cannot remove due to negative result
                raise ValueError('Cannot remove due to negative result')
        raise ValueError('Item does not exist')

    def remove_all_item(self):
        return self.items.all().delete()
    
    def __str__(self) -> str:
        return f'[Cart] {self.account}'


class Item(models.Model):
    cart = models.ForeignKey(to=Cart,on_delete=models.CASCADE,related_name='items')
    note = models.ForeignKey(to=Note,on_delete=models.CASCADE,related_name='+')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f'Note: {self.note.title} : Quantity={self.quantity}'

    def total_price(self):
        return self.note.price*self.quantity

    