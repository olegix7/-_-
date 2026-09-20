"""Auto-create a Profile whenever a new User is saved."""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        # Ensure profile always exists even for legacy users
        Profile.objects.get_or_create(user=instance)
