from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')

    phone = PhoneNumberField()
    
    bachelor = models.CharField(default="", max_length=100)

    rating = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    user_reviews = models.IntegerField(default=0)

    def add_review(self, rating : float) -> None:
        """
        Adds a review to the user.
        """
        self.rating = (self.rating * self.user_reviews + rating) / (self.user_reviews + 1)
        self.user_reviews += 1
        self.save()

    def __str__(self):
        return f"{self.user.username} Info"
