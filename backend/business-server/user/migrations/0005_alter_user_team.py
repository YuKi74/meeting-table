# Generated by Django 3.2.3 on 2021-07-29 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_rename_initroduction_team_introduction'),
        ('user', '0004_alter_user_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_team', to='team.team'),
        ),
    ]
