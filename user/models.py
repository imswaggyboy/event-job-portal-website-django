from django.db import models
from django.contrib.auth.models import User
# from PIL import Image


# Creating profile model with djangoUser extending to add profile image
class Profile(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    ]
    USER_TYPE = [
        ('R', 'Recruiter'),
        ('E', 'Employee')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,default="")
    last_name = models.CharField(max_length=30,default="")
    image = models.ImageField(default='profile_pics/default.jpg',upload_to='profile_pics')
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default="Unknown")
    user_type = models.CharField(max_length=1, choices=USER_TYPE, default="Unknown")



    def __str__(self):
        return f"{self.user.username} Profile"


    # def save(self, *args, **kargs):
    #     super().save(*args, **kargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 200 or img.width > 200:
    #         output_size = (200, 200)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
