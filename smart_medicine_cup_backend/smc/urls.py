from django.urls import path
from landing_page.views import Home
from . import views


urlpatterns = [
    path('info/', views.alarm.register_info),
]
