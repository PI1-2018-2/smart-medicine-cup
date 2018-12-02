 Django
from django.conf.urls import url

# Local Django
from .views import (ListCups
                    )

urlpatterns = (
    url(r'^list_cups/$', ListCups.as_view(), name='list_cups'),
    )