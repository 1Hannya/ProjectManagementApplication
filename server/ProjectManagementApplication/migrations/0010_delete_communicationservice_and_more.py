# Generated by Django 5.0.2 on 2024-02-15 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManagementApplication', '0009_alter_message_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommunicationService',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='idCS',
            new_name='idTask',
        ),
    ]
