from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from notification_telegram.resources import NoteResource

note_resource = NoteResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing_page.urls')),
    path('user/', include('user.urls')),
    url(r'^api/', include(note_resource.urls)),
]
