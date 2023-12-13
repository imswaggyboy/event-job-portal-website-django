from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Jobs(models.Model):
    GENDER_PREFERENCE = [
        ('M','Male'),
        ('F','Female'),
        ('A','ALL'),
    ]
    SHIFT_EVENT = [
        ('D','Day'),
        ('N','Night')
    ]
    DRESS_CODE = [
        ('F','Formal'),
        ('C','Casual')
    ]

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)
    location = models.CharField(max_length=30)
    pay_per_day = models.IntegerField()
    gender_preference = models.CharField(max_length=1,choices=GENDER_PREFERENCE)
    date_of_event = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    age_limit = models.IntegerField()
    duration_of_event = models.IntegerField()
    shift = models.CharField(max_length=1,choices=SHIFT_EVENT)
    dress_code = models.CharField(max_length=1,choices=DRESS_CODE)
    # whatsapp_link = models.CharField(max_length=200)
    description = models.TextField()


    class Meta:
        ordering = ['date_of_event']


    def __str__(self):
        return self.job_title
    
    def get_absolute_url(self):
        return reverse("jobs-detail", kwargs={"pk": self.pk})
    
