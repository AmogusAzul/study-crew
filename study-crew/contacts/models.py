from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contact')

    # Add a ManyToManyField for blocked relationships
    blocked_students = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True
    )

    # Add a ManyToManyField for contact relationships
    friends = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True
    )

    def __str__(self):

        return f"{self.user.username} Contact"

