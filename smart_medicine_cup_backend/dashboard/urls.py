from django.urls import path
from dashboard.views import Dashboard, EditRegistration

urlpatterns = [
    path('', Dashboard.as_view()),
    path('edit_registration/', EditRegistration.as_view()),
]
