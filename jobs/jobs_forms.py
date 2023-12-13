from .models import Jobs
from django import forms


class JobsCreationForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['job_title',
                  'job_type',
                  'location',
                  'pay_per_day',
                  'gender_preference',
                  'date_of_event',
                  'start_time',
                  'end_time',
                  'age_limit',
                  'duration_of_event',
                  'shift',
                  'dress_code',
                  'description']