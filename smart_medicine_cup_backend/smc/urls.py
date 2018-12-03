from django.urls import path
from landing_page.views import Home
from django.conf.urls import url
from . import views


urlpatterns = [
    path('info/', views.alarm.register_info),
    url(r'^signup/$', views.user.signup, name='signup'),
    url(r'^login/$', views.user.user_login, name='login'),
    url(r'^logout/$', views.user.user_logout, name='logout'),
    url(r'^add_smc/$', views.dashboard.add_smc, name='add_smc'),
    url(r'^add_contact/$', views.dashboard.add_contact, name='add_contact'),
]
