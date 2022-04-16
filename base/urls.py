from django.urls import URLPattern, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('opennote', views.open, name='open'),
    path('book', views.book, name="book"),
    path('addnote', views.addnote, name='addnote'),
    path('editnote/<int:id>', views.note_edit_view,name='editnote'),
    path('note/<int:id>',views.note_view,name='note_view'),
    path('cate/<str:cate>',views.cateview, name='cate'),
    path('book/all',views.all,name='all'),
    path('like1/<int:noteid>',views.like1,name='like1'),
    path('profile', views.mypage, name='mypage'),
    path('profile/edit',views.edit_profile_view,name='editprofile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
