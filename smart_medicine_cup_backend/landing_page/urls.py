from django.urls import path
from landing_page.views import Home

urlpatterns = [
    path('', Home.as_view()),
]
