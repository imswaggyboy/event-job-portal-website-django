from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Jobs
from django.contrib.auth.models import User
from chats.models import ChatGroupMember


@receiver(post_save, sender=Jobs)
def add_chat_group_member( sender, instance, created ,**kwargs):
    if created:
        user = User.objects.get(pk=instance.recruiter.id)
        job = instance
        ChatGroupMember.objects.create(group=job,member=user)