from django.urls import path
from user.views import Login, SingUp


urlpatterns = [
    path('login/', Login.as_view()),
    path('signup/', SingUp.as_view()),
]
