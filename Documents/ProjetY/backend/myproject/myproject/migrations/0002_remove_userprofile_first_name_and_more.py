# Generated by Django 4.2.13 on 2024-05-24 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='user',
        ),
        migrations.AddField(
            model_name='validation',
            name='user_profile',
            field=models.OneToOneField(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='validation', to='myproject.userprofile'),
            preserve_default='True',
        ),
    ]
