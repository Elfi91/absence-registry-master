from django.db import models
from django.contrib.auth.models import User
from students.models import Student

class Absence(models.Model): # Deve ereditare da models.Model
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_justified = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
