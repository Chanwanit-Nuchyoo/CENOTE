from django.urls import URLPattern, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('opennote', views.open, name='open'),
    path('book', views.book, name="book"),
    path('addnote', views.addnote, name='addnote'),
    path('note/<int:id>',views.note_view,name='note_view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
