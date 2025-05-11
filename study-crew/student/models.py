from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')

    def __str__(self):
        return f"{self.user.username} Student"

class Subject(models.Model):
    subject_code = models.CharField(max_length=100)
    score = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="subjects")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subject_code', 'student'], name='unique_subject_per_student')
        ]


    def __str__(self):
        return f"({self.subject_code}: {self.score})"
