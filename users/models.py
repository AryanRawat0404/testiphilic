from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=20)
    roll_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} ({self.class_name} - {self.roll_number})"

    class Meta:
        unique_together = ('class_name', 'roll_number')

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    teacher_id =models.AutoField(primary_key=True)
    subject = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.teacher_id} - {self.full_name} ({self.subject})"
    
    class Meta:
        unique_together = ('full_name', 'teacher_id')