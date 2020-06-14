from django.urls import path

from app.pkg.account.api import views


urlpatterns = [
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/change-password', views.ChangePasswordView.as_view(), name='change-password'),
]
