from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.user.signup, name='signup'),
    url(r'^login/$', views.user.user_login, name='login'),
    url(r'^logout/$', views.user.user_logout, name='logout'),
]
