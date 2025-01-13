from django.urls import path

from .import views

urlpatterns = [
    path('login-set-cookie', views.login_set_cookie, name='login-set-cookie'),
]
