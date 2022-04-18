from django.db import models
from account.models import Account
from  base.models import Note


class Cart(models.Model):
    # To get queryset for items in the cart use self.items.all()

    account = models.OneToOneField(Account,on_delete=models.CASCADE,related_name='cart')
    # related_name = ['items',]
    
    def total_price(self):
        price = 0        
        price = sum([item.note.price*item.quantity for item in self.items.all()])
        return price

    def total_quantity(self):
        return sum([item.quantity for item in self.items.all()])
    
    def add_item(self,note,quantity=1):
        if self.items.all().filter(note=note).exists():
            item = self.items.get(note=note)
            item.quantity += quantity
            return item.save()
        return self.items.create(cart=self,note=note,quantity=quantity)

    def remove_item(self,note,quantity=1):
        if self.items.all().filter(note=note).exists():
            item = self.items.get(note=note)
            if item.quantity >= quantity:
                item.quantity -= quantity
                # remove successfully
                if item.quantity == 0:
                    # down to 0
                    return self.item.delete()
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

