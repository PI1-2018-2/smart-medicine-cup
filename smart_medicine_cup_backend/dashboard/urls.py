from django.urls import path
from dashboard.views import Dashboard

urlpatterns = [
    path('', Dashboard.as_view()),
]
