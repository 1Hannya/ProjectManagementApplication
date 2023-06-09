# Generated by Django 4.1.1 on 2023-04-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectManagementApplication', '0002_project_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('idExecutor', models.IntegerField()),
                ('executor', models.CharField(max_length=100)),
                ('responsible', models.CharField(max_length=100)),
                ('dateStart', models.CharField(max_length=10)),
                ('dateEnd', models.CharField(max_length=10)),
                ('link', models.TextField()),
                ('comment', models.TextField()),
                ('idProject', models.IntegerField()),
                ('titleProject', models.TextField()),
                ('state', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='dateEnd',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='project',
            name='dateStart',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.CharField(max_length=10),
        ),
    ]
