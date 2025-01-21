from django.db import models
from django.conf import settings

# Models.py
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.created_by:
            self.created_by = f"uid{self.id}"
            super().save(update_fields=['created_by'])

    def __str__(self):
        return self.name

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects',null=False, blank=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project_type = models.CharField(max_length=255)
    project_id = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.project_id:
            self.project_id = f"pid{self.id}"
            super().save(update_fields=['project_id'])

    def __str__(self):
        return self.name

class TestCase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_cases',null=False, blank=False)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

class TestSuite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='test_suites',null=False, blank=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    pre_requisite = models.TextField(null=True, blank=True)
    labels = models.JSONField(null=True, blank=True, default=list)  # Use JSONField to store lists


    def __str__(self):
        return self.title

class Requirement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="requirements")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=[('Functional', 'Functional'), ('Non-Functional', 'Non-Functional'), ('Regression', 'Regression')])
    start_date = models.DateField()
    completion_date = models.DateField()
    labels = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title 