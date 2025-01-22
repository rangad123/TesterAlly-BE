from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet,TestCaseViewSet,TestSuiteViewSet,RequirementViewSet
from .views import RegisterView, LoginView, ForgotPasswordView, ResetPasswordView
from .views import TestCaseTypeViewSet, TestCasePriorityViewSet, RequirementTypeViewSet
from .views import UserListView, ProjectListView, TestCaseListView, TestSuiteListView, RequirementListView, RoleView

# Router for viewsets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'testcases', TestCaseViewSet, basename='testcase')
router.register(r'testsuites', TestSuiteViewSet, basename='testsuite')
router.register(r'requirements', RequirementViewSet, basename='requirement')
router.register(r'testcase-types', TestCaseTypeViewSet,basename='test-type')
router.register(r'testcase-priorities', TestCasePriorityViewSet,basename='test-priorities')
router.register(r'requirement-types', RequirementTypeViewSet,basename='requirements-type')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgotPassword/', ForgotPasswordView.as_view(), name='forgotPassword'),
    path('resetPassword/', ResetPasswordView.as_view(), name='resetPassword'),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('admin/projects/', ProjectListView.as_view(), name='project-list'),
    path('admin/testcases/', TestCaseListView.as_view(), name='testcase-list'),
    path('admin/testsuites/', TestSuiteListView.as_view(), name='testsuite-list'),
    path('admin/requirements/', RequirementListView.as_view(), name='requirement-list'),
    path('admin/roles/', RoleView.as_view(), name='role-management'),

]

# Include router URLs for viewsets
urlpatterns += router.urls