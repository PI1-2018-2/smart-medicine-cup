from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view()),
    path('registration/', views.Registration.as_view()),
    path('edit_registration/', views.EditRegistration.as_view()),
    path('login/', views.Login.as_view()),
]
