from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def save_profile(sender, instance ,created , **kwargs):
    user = instance
    if created:
        profile = Profile(user =user)
        profile.save()
        # Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance ,**kwargs):
#         instance.profile.save()





    