"""
URL configuration for expenseswebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register',RegistrationView.as_view(),name="register"),
    path('logout',LogoutView.as_view(),name = "logout"),
    path('validate-username',csrf_exempt(UserNameValidationView.as_view()),name='validate-username'),
    path('password-strength',csrf_exempt(PasswordStrengthView.as_view()),name="password-strength"),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
    path('activate/<uibd64>/<token>',VerificationView.as_view(),name="activate"),
    path('login',LoginView.as_view(),name="login"),
    path('request-reset-link',RequestPasswordResetEmail.as_view(),name='request-password'),
    path('reset-user-password/<uibd64>/<token>',CompletePasswordReset.as_view(),name="reset-user-password"),
    # path('register',views.register,name="register")
]
