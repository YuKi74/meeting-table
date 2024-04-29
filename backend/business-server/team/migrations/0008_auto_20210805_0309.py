# Generated by Django 3.2.3 on 2021-08-05 03:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0007_meetingroom_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingroomfiles',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meetingroomfiles',
            name='time',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
