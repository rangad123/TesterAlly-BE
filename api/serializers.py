from rest_framework import serializers
from .models import User, Project, TestCase, TestSuite

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'phone', 'country', 'created_by']
        extra_kwargs = {'password': {'write_only': True}}

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_id', 'name', 'description', 'project_type','user_id']

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'name', 'url', 'project_id']

class TestSuiteSerializer(serializers.ModelSerializer):
    labels = serializers.ListField(
        child=serializers.CharField()  # Ensure the child field is a string (CharField)
    )
    class Meta:
        model = TestSuite
        fields = ['id', 'title', 'description', 'pre_requisite', 'labels', 'project_id']
