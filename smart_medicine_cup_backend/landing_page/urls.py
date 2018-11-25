from django.urls import path
from landing_page.views import Home, Team

urlpatterns = [
    path('', Home.as_view()),
    path('team/', Team.as_view()),
]
