from django.urls import path
from landing_page.views import Home
from django.conf.urls import url
from . import views


urlpatterns = [
    path('info/', views.alarm.register_info),
    url(r'^signup/$', views.user.signup, name='signup'),
]
