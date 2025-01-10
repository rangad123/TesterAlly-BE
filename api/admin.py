from django.contrib import admin
from .models import User
from .models import Project, TestCase, TestSuite

# Register your models here.

admin.site.register(User)

admin.site.register(Project)
admin.site.register(TestCase)
admin.site.register(TestSuite)
