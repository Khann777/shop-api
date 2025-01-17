from django.urls import path

from .views import RegisterView, ActivateView, LoginView, LogoutView, ResetPasswordView, RefreshView, \
    PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/', ActivateView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('refresh-token/', RefreshView.as_view(), name='refresh-token'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
]