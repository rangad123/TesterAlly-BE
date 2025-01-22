from rest_framework import serializers
from .models import User, Project, TestCase, TestSuite,Requirement,Role
from .models import TestCaseType, TestCasePriority, RequirementType

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'phone', 'country', 'created_by']
        extra_kwargs = {'password': {'write_only': True}}

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_id', 'name', 'description', 'project_type','user_id']

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'name', 'url', 'project_id', 'testcase_type', 'testcase_priority']

class TestSuiteSerializer(serializers.ModelSerializer):
    labels = serializers.ListField(
        child=serializers.CharField()  # Ensure the child field is a string (CharField)
    )
    testcase = serializers.ListField(
        child=serializers.CharField(), required=False  # Allow single or multiple test cases
    )
    class Meta:
        model = TestSuite
        fields = ['id', 'title', 'description', 'pre_requisite', 'labels', 'project_id', 'testcases']

class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['id', 'project_id', 'title', 'description', 'type', 'start_date', 'completion_date', 'labels']


#Database types Serializers

class TestCaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCaseType
        fields = '__all__'

class TestCasePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCasePriority
        fields = '__all__'

class RequirementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementType
        fields = '__all__'