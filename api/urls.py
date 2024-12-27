from django.urls import path
from .views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgotPassword/', ForgotPasswordView.as_view(), name='forgotPassword'),
    path('resetPassword/', ResetPasswordView.as_view(), name='resetPassword'),
]
