# Generated by Django 4.2.7 on 2023-11-21 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_jobs_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='whatsapp_link',
        ),
    ]
