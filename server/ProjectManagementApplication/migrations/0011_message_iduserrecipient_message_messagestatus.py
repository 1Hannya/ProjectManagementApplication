# Generated by Django 5.0.2 on 2024-03-27 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManagementApplication', '0010_delete_communicationservice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='idUserRecipient',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='messageStatus',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
