# Generated by Django 4.2.2 on 2023-11-11 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200)),
                ('job_type', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=30)),
                ('pay_per_day', models.IntegerField()),
                ('gender_preference', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('A', 'ALL')], max_length=1)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('age_limit', models.IntegerField()),
                ('duration_of_event', models.IntegerField()),
                ('shift', models.CharField(choices=[('D', 'Day'), ('N', 'Night')], max_length=1)),
                ('dress_code', models.CharField(choices=[('F', 'Formal'), ('C', 'Casual')], max_length=1)),
                ('whatsapp_link', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-job_title'],
            },
        ),
    ]
