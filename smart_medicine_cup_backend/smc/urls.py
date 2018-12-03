from django.urls import path
from landing_page.views import Home
from django.conf.urls import url
from . import views


urlpatterns = [
    path('info/', views.alarm.register_info),
    path('get_record/', views.alarm.get_record),
    path('get_contact/', views.alarm.get_contact),
    url(r'^signup/$', views.user.signup, name='signup'),
    url(r'^login/$', views.user.user_login, name='login'),
    url(r'^logout/$', views.user.user_logout, name='logout'),
    url(r'^add_smc/$', views.dashboard.add_smc, name='add_smc'),
]
