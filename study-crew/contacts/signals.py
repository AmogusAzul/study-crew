from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Contact

@receiver(post_save, sender=User)
def create_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_contact(sender, instance, **kwargs):
    instance.student.save()