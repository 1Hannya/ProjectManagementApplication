# Generated by Django 4.1.7 on 2023-05-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManagementApplication', '0003_task_alter_project_dateend_alter_project_datestart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='comment',
            field=models.TextField(default=-2000),
            preserve_default=False,
        ),
    ]
