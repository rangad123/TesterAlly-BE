from rest_framework import serializers
from .models import User
from .models import Project, TestCase, TestSuite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'phone', 'country']
        extra_kwargs = {'password': {'write_only': True}}


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'project_type']

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'name', 'url']

class TestSuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSuite
        fields = ['id', 'title', 'description', 'pre_requisite', 'labels']