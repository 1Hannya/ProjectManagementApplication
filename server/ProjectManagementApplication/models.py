from django.db import models

class User(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    number = models.CharField(max_length=11)
    birthday = models.CharField(max_length=10)
    note = models.TextField()
    visual = models.IntegerField()
    style = models.CharField(max_length=10)


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
    description = models.TextField()

class Task(models.Model):
    title = models.CharField(max_length=150)
    idExecutor = models.IntegerField()
    executorName = models.CharField(max_length=100)
    idResponsible = models.IntegerField()
    responsibleName = models.CharField(max_length=100)
    dateStart = models.CharField(max_length=10)
    dateEnd = models.CharField(max_length=10)
    link = models.TextField()
    description = models.TextField()
    idProject = models.IntegerField()
    titleProject = models.TextField()
    state = models.CharField(max_length=20)

class Message(models.Model):
    idTask = models.IntegerField()
    messageText = models.TextField()
    date = models.TextField()
    idUser = models.IntegerField()
    userName = models.CharField(max_length=100)
    idUserRecipient = models.IntegerField()
    messageStatus = models.IntegerField()



