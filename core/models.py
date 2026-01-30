from django.db import models
from django.contrib.auth.models import User
from students.models import Student

class Absence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="absences")
    date = models.DateField()
    is_justified = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

