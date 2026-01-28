from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    role_choices = (
        ('principal', 'Principal'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete= models.CASCADE)
    role = models.CharField(max_length= 20, choices= role_choices)

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
    