from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from notification_telegram.resources import NotificationResource

note_resource = NotificationResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing_page.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('user/', include('user.urls')),
    url(r'^api/', include(note_resource.urls)),
]
