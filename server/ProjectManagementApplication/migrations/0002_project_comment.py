# Generated by Django 4.1.1 on 2023-04-08 06:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManagementApplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='comment',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
