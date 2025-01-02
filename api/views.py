from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
import uuid

from .models import User
from .serializers import UserSerializer


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
            country=data['country']
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

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"success": True, "message": "You have access to this protected view!"},
            status=status.HTTP_200_OK
        )
