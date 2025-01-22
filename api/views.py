from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from .models import Project, TestCase, TestSuite, Requirement
from .serializers import ProjectSerializer, TestCaseSerializer, TestSuiteSerializer, RequirementSerializer, RoleSerializer
from django.contrib.sites.shortcuts import get_current_site
import uuid
from .models import User, Role
from .serializers import UserSerializer


class RoleView(APIView):
    def get(self, request):
        """
        Retrieve all roles.
        """
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new role.
        Restrict creation to the predefined roles.
        """
        predefined_roles = {1: "Admin", 2: "Organization", 3: "Project Member"}
        role_id = request.data.get("id")
        role_name = request.data.get("name")

        # Check if the role ID is within the predefined range
        if role_id not in predefined_roles:
            return Response({"error": "Invalid role ID. Allowed IDs are 1, 2, and 3."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the role name matches the predefined role for the given ID
        if predefined_roles[role_id] != role_name:
            return Response({"error": f"Role name must be '{predefined_roles[role_id]}' for ID {role_id}."}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the role
        role, created = Role.objects.get_or_create(id=role_id, defaults={"name": role_name})
        if not created:
            return Response({"message": "Role already exists."}, status=status.HTTP_200_OK)

        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#Register Api
class RegisterView(APIView):
    def post(self, request):
        data = request.data

        
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {"success": False, "message": "Email is already registered."},
                status=status.HTTP_400_BAD_REQUEST
            )

       
        hashed_password = make_password(data['password'])

        
        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            phone=data['phone'],
            country=data['country'],
            role_id=data['roleid']
        )

        serializer = UserSerializer(user)
        return Response(
            {"success": True, "message": "User registered successfully!", "user": serializer.data},
            status=status.HTTP_201_CREATED
        )



#Login View Api
class LoginView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(email=data['email'])
            if check_password(data['password'], user.password):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "success": True,
                        "message": "Login successful!",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "user": {
                            "id":user.id,
                            "roleId":user.role_id,
                            "name": user.name,
                            "email": user.email
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"success": False, "message": "Invalid credentials."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST
            )


# forgotPassword Api
class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(email=data['email'])
            
            
            token = str(uuid.uuid4())
            user.reset_token = token  
            user.save()

            current_site = get_current_site(request)
            reset_link = f"https://testerally-fe.onrender.com/resetPassword/{token}"

            send_mail(
                'Password Reset Request',
                f'Click here to reset your password: {reset_link}',  # Reset link
                'suriya.prakash@crowd4test.com',  # From email address
                [data['email']],  # User's email
                fail_silently=False,
            )

            return Response(
                {
                    "success": True,
                    "message": "Password reset link has been sent to your email.",
                    "reset_link": reset_link  # For testing purposes
                },
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "Email not found."},
                status=status.HTTP_400_BAD_REQUEST
            )


#ResetPassword Api
class ResetPasswordView(APIView):
    def post(self, request):
        data = request.data
        try:
            
            user = User.objects.get(reset_token=data['uuid'])
            
            
            user.password = make_password(data['password'])
            
            
            user.reset_token = None
            user.save()

            return Response(
                {"success": True, "message": "Password reset successful."}, 
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "Invalid or expired token."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

#Admin View api for Frontend

class UserListView(APIView):

    def get(self, request):
        # Fetch all users from the database
        users = User.objects.all()
        
        # Serialize the data
        serializer = UserSerializer(users, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectListView(APIView):
    def get(self,request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TestCaseListView(APIView):
    def get (self,request):
        testcases = TestCase.objects.all()
        serializer = TestCaseSerializer(testcases,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class TestSuiteListView(APIView):
    def get(self,request):
        test_suites = TestSuite.objects.all()
        serializer = TestSuiteSerializer(test_suites,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class RequirementListView(APIView):
    def get(self,request):
        requirements = Requirement.objects.all()
        serializer = RequirementSerializer(requirements,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



#User Main api for Frontend

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # Filter projects by the logged-in user's ID
        user_id = self.request.query_params.get('user_id')  # Use query_params for GET requests

        if not user_id:
            raise ValidationError("User Id is required in query parameters.")
            
        return Project.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.request.data.get("user_id")  # Get the user ID from the authenticated user
        # Ensure name, description, and project_type are passed
        name = self.request.data.get('name')
        description = self.request.data.get('description')
        project_type = self.request.data.get('project_type')

        if not name or not description or not project_type:
            raise ValidationError("Name, description, and project type are required.")
        
        # Save the project with the correct user_id
        serializer.save(user_id=user_id)

    def _get_project_for_user(self, project_id, user_id):
        """Helper method to validate and fetch the project linked to the user."""
        try:
            project = Project.objects.get(id=project_id, user_id=user_id)
            return project
        except Project.DoesNotExist:
            raise ValidationError("Project does not exist or is not linked to the user.")




class TestCaseViewSet(viewsets.ModelViewSet):
    serializer_class = TestCaseSerializer

    def get_queryset(self):
        user_id = self.request.user.id  # Get the user ID from the authenticated user
        project_id = self.request.query_params.get('project_id')  # Use query parameters for GET

        if not project_id:
            raise ValidationError("Project ID is required in query parameters.")

        return TestCase.objects.filter(project__id=project_id)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        project_id = self.request.data.get('project_id')

        if not project_id:
            raise ValidationError("Project ID is required.")
        
        # Use the helper method to ensure the project is valid for the user
        project = self._get_project_for_user(project_id)

        # Save the test case with the correct project and user
        serializer.save(project=project)

    def _get_project_for_user(self, project_id):
        try:
            project = Project.objects.get(id=project_id)
            return project
        except Project.DoesNotExist:
            raise ValidationError("Project not found or does not belong to the user.")


class TestSuiteViewSet(viewsets.ModelViewSet):
    serializer_class = TestSuiteSerializer

    def get_queryset(self):
        user_id = self.request.user.id  # Get the user ID from the authenticated user
        project_id = self.request.query_params.get('project_id')  # Use query parameters for GET

        if not project_id:
            raise ValidationError("Project ID is required in query parameters.")

        return TestSuite.objects.filter(project__id=project_id)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        project_id = self.request.data.get('project_id')

        if not project_id:
            raise ValidationError("Project ID is required.")
        
        # Use the helper method to ensure the project is valid for the user
        project = self._get_project_for_user(project_id)

        # Save the test suite with the correct project and user
        serializer.save(project=project)

    def _get_project_for_user(self, project_id):
        try:
            project = Project.objects.get(id=project_id)
            return project
        except Project.DoesNotExist:
            raise ValidationError("Project not found or does not belong to the user.")


class RequirementViewSet(viewsets.ModelViewSet):
    serializer_class = RequirementSerializer

    def get_queryset(self):
        # Filter requirements by the logged-in user's projects
        user_id = self.request.user.id
        project_id = self.request.query_params.get('project_id')  # Use query parameters for GET

        if not project_id:
            raise ValidationError("Project ID is required in query parameters.")

        return Requirement.objects.filter(project__id=project_id)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        project_id = self.request.data.get('project_id')

        if not project_id:
            raise ValidationError("Project ID is required.")
        
        # Use the helper method to ensure the project is valid for the user
        project = self._get_project_for_user(project_id)

        start_date = self.request.data.get('start_date')
        completion_date = self.request.data.get('completion_date')

        # Validate that completion date is after start date
        if start_date and completion_date and start_date > completion_date:
            raise ValidationError("Completion date must be after start date.")

        # Save the requirement with the correct project
        serializer.save(project=project)

    def _get_project_for_user(self, project_id):
        """Helper method to validate and fetch the project linked to the user."""
        try:
            project = Project.objects.get(id=project_id)
            return project
        except Project.DoesNotExist:
            raise ValidationError("Project not found or does not belong to the user.")



# Protected View for authenticated users
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"success": True, "message": "You have access to this protected view!"},
            status=status.HTTP_200_OK
        )