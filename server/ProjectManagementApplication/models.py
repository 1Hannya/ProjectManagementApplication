from django.db import models

class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    number = models.CharField(max_length=11)
    birthday = models.CharField(max_length=10)
    comment = models.TextField()

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Project(models.Model):
    title = models.CharField(max_length=150)
    clientName = models.CharField(max_length=100)
    dateStart = models.CharField(max_length=10)
    email = models.EmailField()
    number = models.CharField(max_length=11)
    dateEnd = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    link = models.TextField()
    comment = models.TextField()

class Task(models.Model):
    title = models.CharField(max_length=150)
    idExecutor = models.IntegerField()
    executor = models.CharField(max_length=100)
    responsible = models.CharField(max_length=100)
    dateStart = models.CharField(max_length=10)
    dateEnd = models.CharField(max_length=10)
    link = models.TextField()
    comment = models.TextField()
    idProject = models.IntegerField()
    titleProject = models.TextField()
    state = models.CharField(max_length=20)

