# Generated by Django 4.2.2 on 2023-11-11 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='date_of_event',
            field=models.DateField(null=True),
        ),
    ]
