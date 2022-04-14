from django.contrib import admin
# Register your models here.

from .models import Note,Comment,Category,Images

admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Images)