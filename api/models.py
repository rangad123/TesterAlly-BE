from django.db import models
from django.conf import settings


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project_type = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TestCase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_cases')
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

class TestSuite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_suites')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    pre_requisite = models.TextField(null=True, blank=True)
    labels = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title