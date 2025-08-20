from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User) #when a user is saved, the create_profile function will be called
def create_profile(sender, instance, created, **kwargs): #*kwargs just accepts any additional arguments
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User) #when a user is saved, the create_profile function will be called
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
