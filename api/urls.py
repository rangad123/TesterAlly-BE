from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet,TestCaseViewSet,TestSuiteViewSet
from .views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView

# Router for viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'testcases', TestCaseViewSet, basename='testcase')
router.register(r'testsuites', TestSuiteViewSet, basename='testsuite')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgotPassword/', ForgotPasswordView.as_view(), name='forgotPassword'),
    path('resetPassword/', ResetPasswordView.as_view(), name='resetPassword'),
]

# Include router URLs for viewsets
urlpatterns += router.urls