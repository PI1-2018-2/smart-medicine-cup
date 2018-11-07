from django.urls import path
from user.views import Login


urlpatterns = [
    path('login/', Login.as_view()),
]
