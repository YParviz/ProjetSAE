# Generated by Django 4.2.13 on 2024-06-08 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0003_alter_validation_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('address', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('accuracy', models.FloatField(blank=True, null=True)),
                ('risk', models.FloatField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
            ],
        ),
    ]