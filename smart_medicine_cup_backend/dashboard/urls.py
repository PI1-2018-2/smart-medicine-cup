from django.urls import path
from dashboard.views import Dashboard, Registration

urlpatterns = [
    path('', Dashboard.as_view()),
    path('registration/', Registration.as_view()),
]
