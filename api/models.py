from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

