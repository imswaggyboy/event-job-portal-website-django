from django.db import models
from jobs.models import *
from django.contrib.auth.models import User

# Create your models here.
class ChatGroup(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

class JoinRequestChatroom(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs,on_delete=models.CASCADE)



class ChatGroupMember(models.Model):
    group = models.ForeignKey(Jobs,on_delete=models.CASCADE)
    member = models.ForeignKey(User,on_delete=models.CASCADE)