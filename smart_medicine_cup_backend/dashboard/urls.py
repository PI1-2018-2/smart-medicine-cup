from django.urls import path
from dashboard import views

urlpatterns = [
    path('', views.Dashboard.as_view()),
    path('edit_registration/', views.EditRegistration.as_view()),
    path('login/', views.Login.as_view()),
    path('smc/', views.Smc.as_view()),
    path('historic/', views.Historic.as_view()),
    path('addsmc/', views.AddSmc.as_view(), name='addsmc'),
]
