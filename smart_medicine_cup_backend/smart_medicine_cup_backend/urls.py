from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include

from smc.resources import RecordResource
record_resource = RecordResource()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing_page.urls')),
    path('api/', include('smc.urls')),
    path('dashboard/', include('dashboard.urls')),
    url(r'^notification/', include(record_resource.urls)),
]
