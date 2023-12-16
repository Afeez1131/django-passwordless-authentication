from django.urls import path
from . import views

app_name = 'password'

urlpatterns = [
    path('home', views.homepage, name='home'),
    path('one-time-login', views.one_time_login, name='one_time_login'),
    path('p-login/<token>', views.passwordless_login, name='passwordless_login'),
]