from datetime import datetime
from passlib.hash import pbkdf2_sha256
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse
from .models import User, Tag, Project, Task, Message
from .form import RegForm, NewProjectForm, NewTaskForm, MainSpaceForm
from django.core.paginator import *
from sys import getdefaultencoding

#Главная
def index(request):
    try:
        userList = User.objects.all()
        name = request.session['name']
        login = request.session['login']
        tag = request.session['tag']
        messageList = list()
        form = MainSpaceForm()
        user = User.objects.get(login=request.session['login'])
        visual = user.visual
        note = user.note
        if request.method == "POST":
            user.note = request.POST.get("note")
            user.save()
            return HttpResponseRedirect("/")
        taskListAccepted = Task.objects.filter(idExecutor=user.id, state="Принята")
        taskListInWork = Task.objects.filter(idExecutor=user.id, state="В работе")
        taskListStoped = Task.objects.filter(idExecutor=user.id, state="Приостановлена")
        taskListAccompaniment = Task.objects.filter(idExecutor=user.id, state="Сопровождение")
        taskListCompleted = Task.objects.filter(idExecutor=user.id, state="Сделана")
        taskList = Task.objects.filter(idExecutor=user.id).exclude(state="В планах")
        paginator = Paginator(taskList, 20)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        dateNow = datetime.now()
        date = dateNow.strftime("%d.%m.%Y")
        msgState=1
        messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
        for msg in messages:
            if(msg.messageStatus == 0):
                messageList.append(msg)
        if(len(messageList)==0):
            msgState = 0
        upcomingTasksList = Task.objects.filter(dateEnd=str(date)).filter(idExecutor=user.id)
        paginator1 = Paginator(upcomingTasksList, 3)
        pageNumber1 = request.GET.get('page')
        pageObj1 = paginator1.get_page(pageNumber1)
        return render(request, "index.html",
                      {"tag": tag, "name": name, "login": login, "visual": visual, "form": form, "note": note,
                       "tasks": taskList, "pageObj": pageObj, "userList": userList, "upcomingTasksList": upcomingTasksList,
                       "pageObj1": pageObj1, "taskListAccepted": taskListAccepted, "taskListInWork": taskListInWork,
                       "taskListStoped": taskListStoped, "taskListCompleted": taskListCompleted,
                       "taskListAccompaniment": taskListAccompaniment, "messageList": messageList, "msgState": msgState,
                       "taskAcceptedCount": taskListAccepted.count(), "taskInWorkCount": taskListInWork.count(),
                       "taskStopedCount": taskListStoped.count(), "taskCompletedCount": taskListCompleted.count(),
                       "taskAccompanimentCount": taskListAccompaniment.count(), "taskCount": taskList.count()})
    except:
        request.session['name'] = 'Неавторизованный пользователь'
        request.session['login'] = "none"
        request.session['tag'] = "guest"
        tag = request.session['tag']
        login = request.session['login']
        name = request.session['name']
        return render(request, "index.html",{"tag": tag, "name": name, "login": login})
#КонецГлавная

#ВизуалТаблиц
def editVisual0(request):
    name = request.session['name']
    login = request.session['login']
    tag = request.session['tag']
    form = MainSpaceForm()
    user = User.objects.get(login=request.session['login'])
    user.visual = 0
    user.save()
    return HttpResponseRedirect("/")
def editVisual1(request):
    name = request.session['name']
    login = request.session['login']
    tag = request.session['tag']
    form = MainSpaceForm()
    user = User.objects.get(login=request.session['login'])
    user.visual = 1
    user.save()
    return HttpResponseRedirect("/")
def editVisualAll0(request, id):
    name = request.session['name']
    login = request.session['login']
    tag = request.session['tag']
    form = MainSpaceForm()
    user = User.objects.get(login=request.session['login'])
    user.visual = 0
    user.save()
    return HttpResponseRedirect("/projects/tasks/"+ str(id) +"/")
def editVisualAll1(request, id):
    name = request.session['name']
    login = request.session['login']
    tag = request.session['tag']
    form = MainSpaceForm()
    user = User.objects.get(login=request.session['login'])
    user.visual = 1
    user.save()
    return HttpResponseRedirect("/projects/tasks/"+ str(id) +"/")
#КонецВизуалТаблиц

#Регистарция
def registrationForAdmin(request):
    if request.method == "GET":
        form = RegForm()
        return render(request, "registrationForAdmin.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login']})
    elif request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            j=1
            user = User()
            user.login = request.POST.get("login")
            password = request.POST.get("password")
            user.name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.number = request.POST.get("number")
            user.birthday = request.POST.get("birthday")
            user.tag = "Администратор"
            user.visual = 0
            user.style = 1
            users = User.objects.all()
            for i in users:
                if str(i.login) == request.POST.get("login"):
                    j = 0
                    break
            if (user.login != '' and password != '' and user.name != '' and '@' in request.POST.get("email") and j == 1):
                user.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
                user.save()
                return HttpResponseRedirect("/personalArea/")
            else:
                errorMsg = "Выбранный вами логин уже используется или вы допустили другую ошибку при создании аккаунта:\n- поле \"ФИО\" осталось пустым\n- поле \"Логин\" осталось пустым\n- поле \"Пароль\" не соответствует требованиям\n- поле \"E-mail\" не содержит домена"
                return render(request, "registrationForAdmin.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "errorMsg": errorMsg})
    errorMsg = "Выбранный вами логин уже используется или вы допустили другую ошибку при создании аккаунта:\n- поле \"ФИО\" осталось пустым\n- поле \"Логин\" осталось пустым\n- поле \"Пароль\" не соответствует требованиям\n- поле \"E-mail\" не содержит домена"
    return render(request, "registrationForAdmin.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "errorMsg": errorMsg})

def registration(request):
    if request.method == "GET":
        form = RegForm()
        return render(request, "registration.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login']})
    elif request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            j=1
            user = User()
            user.login = request.POST.get("login")
            password = request.POST.get("password")
            user.name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.number = request.POST.get("number")
            user.birthday = request.POST.get("birthday")
            user.tag = "Пользователь"
            user.visual = 0
            user.style = 1
            users = User.objects.all()
            for i in users:
                if str(i.login) == request.POST.get("login"):
                    j=0
                    break
            if (user.login != '' and password != '' and user.name != '' and '@' in request.POST.get("email") and j == 1):
                user.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
                user.save()
                return HttpResponseRedirect("/personalArea/")
            else:
                errorMsg = "Выбранный вами логин уже используется или вы допустили другую ошибку при создании аккаунта:\n- поле \"ФИО\" осталось пустым\n- поле \"Логин\" осталось пустым\n- поле \"Пароль\" не соответствует требованиям\n- поле \"E-mail\" не содержит домена"
                return render(request, "registration.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "errorMsg": errorMsg})
    errorMsg = "Выбранный вами логин уже используется или вы допустили другую ошибку при создании аккаунта:\n- поле \"ФИО\" осталось пустым\n- поле \"Логин\" осталось пустым\n- поле \"Пароль\" не соответствует требованиям\n- поле \"E-mail\" не содержит домена"
    return render(request, "registration.html", {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "form": form, "errorMsg": errorMsg})

def validate_login(request):
    login = request.GET.get('login', None)
    response = {
        'is_taken': User.objects.filter(login=login).exists()
    }
    return JsonResponse(response)
#КонецРегистарция

#АвторизацияИВыход
def login(request):
    errorMsg = None
    try:
        if request.method == "POST":
            login = request.POST.get("login")
            password = request.POST.get("password")
            userForSession = User.objects.get(login = login)
            if (pbkdf2_sha256.verify(password, userForSession.password)):
                request.session['name'] = userForSession.name
                request.session['login'] = userForSession.login
                request.session['tag'] = userForSession.tag
                return HttpResponseRedirect("/")
            else:
                errorMsg = "Введен неверный логин и/или пароль"
                return render(request, "login.html", {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "errorMsg": errorMsg})
        else:
            return render(request, "login.html", {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login']})
    except User.DoesNotExist:
        errorMsg = "Введен неверный логин и/или пароль"
        return render(request, "login.html", {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "errorMsg": errorMsg})

def logout(request):
    try:
        request.session['name'] = 'Неавторизованный пользователь'
        request.session['login'] = "none"
        request.session['tag'] = "guest"
    except KeyError:
        pass
    return HttpResponseRedirect("/")
#КонецАвторизацияИВыход

#ЛичныйКабинет
def editUser(request):
    if request.session['login'] == "none":
        return HttpResponse('У вас нет доступа к этой странице')
    else:
        try:
            messageList = list()
            tagList = Tag.objects.all()
            paginator = Paginator(tagList, 20)
            pageNumber = request.GET.get('page')
            pageObj = paginator.get_page(pageNumber)
            user = User.objects.get(login=request.session['login'])
            msgState = 1
            messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
            for msg in messages:
                if (msg.messageStatus == 0):
                    messageList.append(msg)
            if (len(messageList) == 0):
                msgState = 0
            if request.POST:
                if 'tag' in request.POST:
                    tag = Tag()
                    tag.name = request.POST.get("tagName")
                    tag.save()
                    return HttpResponseRedirect("/personalArea/")
                elif 'user' in request.POST:
                    password = request.POST.get("password")
                    if (request.POST.get("name") != '' and request.POST.get("login") != '' and password != '' and len(password) >= 6 and '@' in request.POST.get("email") and len(request.POST.get("number"))>=6):
                        users = User.objects.filter(login__exact = str(request.POST.get("login")))
                        if (len(users) == 0):
                            user.name = request.POST.get("name")
                            user.login = request.POST.get("login")
                            user.number = request.POST.get("number")
                            user.email = request.POST.get("email")
                            user.birthday = request.POST.get("birthday")
                            user.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
                            user.save()
                            request.session['name'] = user.name
                            request.session['login'] = user.login
                        elif (request.POST.get("login") == request.session['login']):
                            user.name = request.POST.get("name")
                            user.login = request.POST.get("login")
                            user.number = request.POST.get("number")
                            user.email = request.POST.get("email")
                            user.birthday = request.POST.get("birthday")
                            user.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
                            user.save()
                            request.session['name'] = user.name
                            request.session['login'] = user.login
                        else:
                             errorMsg = "Введенный логин уже занят"
                             return render(request, "personalArea.html", {"user": user, "tagList": tagList, "pageObj": pageObj, "tag": request.session['tag'],
                                            "name": request.session['name'],  "messageList": messageList, "msgState": msgState, "login": request.session['login'], "errorMsg": errorMsg})
                    elif (request.POST.get("name") != '' and request.POST.get("login") != '' and password == '' and '@' in request.POST.get("email") and len(request.POST.get("number"))>=6):
                        users = User.objects.filter(login__exact  = str(request.POST.get("login")))
                        if (len(users) == 0):
                            user.name = request.POST.get("name")
                            user.login = request.POST.get("login")
                            user.number = request.POST.get("number")
                            user.email = request.POST.get("email")
                            user.birthday = request.POST.get("birthday")
                            user.save()
                            request.session['name'] = user.name
                            request.session['login'] = user.login
                        elif (request.POST.get("login") == request.session['login']):
                            user.name = request.POST.get("name")
                            user.login = request.POST.get("login")
                            user.number = request.POST.get("number")
                            user.email = request.POST.get("email")
                            user.birthday = request.POST.get("birthday")
                            user.save()
                            request.session['name'] = user.name
                            request.session['login'] = user.login
                        else:
                            errorMsg = "Введенный логин уже занят"
                            return render(request, "personalArea.html", {"user": user, "tagList": tagList, "pageObj": pageObj, "tag": request.session['tag'],
                                        "name": request.session['name'],  "messageList": messageList, "msgState": msgState, "login": request.session['login'], "errorMsg": errorMsg})
                    else:
                        errorMsg = "Введены некорректные данные:\n- поле \"Ваше имя\" осталось пустым\n- поле \"Ваш логин\" осталось пустым\n- поле \"Пароль\" не соответствует требованиям\n- поле \"E-mail\" не содержит домена"
                        return render(request, "personalArea.html", {"user": user, "tagList": tagList, "pageObj": pageObj, "tag": request.session['tag'],
                                    "name": request.session['name'],  "messageList": messageList, "msgState": msgState, "login": request.session['login'], "errorMsg": errorMsg})
                return render(request, "personalArea.html", {"user": user, "tagList": tagList, "pageObj": pageObj, "tag": request.session['tag'],
                            "name": request.session['name'],  "messageList": messageList, "msgState": msgState, "login": request.session['login']})
            else:
                return render(request, "personalArea.html", {"user": user, "tagList": tagList, "pageObj": pageObj, "tag": request.session['tag'],
                            "name": request.session['name'],  "messageList": messageList, "msgState": msgState, "login": request.session['login']})
        except User.DoesNotExist:
            return HttpResponseNotFound("<h2>Пользователь не найден</h2>")

def deleteTag(request, id):
    try:
        tag = Tag.objects.get(id=id)
        tag.delete()
        return HttpResponseRedirect("/personalArea/")
    except Tag.DoesNotExist:
        return HttpResponseNotFound("<h2>Тэг не найден</h2>")
#КонецЛичныйКабинет

#Тэги
def tagUsers(request):
    user = User.objects.get(login=request.session['login'])
    messageList = list()
    msgState = 1
    messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
    for msg in messages:
        if (msg.messageStatus == 0):
            messageList.append(msg)
    if (len(messageList) == 0):
        msgState = 0
    objects = list(Tag.objects.all())
    usersList = User.objects.all()
    paginator = Paginator(usersList, 10)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    return render(request, "tagUsers.html",
                      {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "messageList": messageList, "msgState": msgState, "usersList": usersList, "pageObj": pageObj, "tagList": objects})

def saveEdit(request, id, tag):
    try:
        user = User.objects.get(id=id)
        user.tag = tag
        if (user.tag != ''):
            user.save()
            return HttpResponseRedirect("/tagUsers/")
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>Пользователь не найден</h2>")

def delete(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return HttpResponseRedirect("/tagUsers/")
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>Пользователь не найден</h2>")
#КонецТэги

#ДействияСПроектами
def projectsForm(request):
    user = User.objects.get(login=request.session['login'])
    messageList = list()
    msgState = 1
    messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
    for msg in messages:
        if (msg.messageStatus == 0):
            messageList.append(msg)
    if (len(messageList) == 0):
        msgState = 0
    projectsList = Project.objects.exclude(state="Сдан")
    completedProjectsList = Project.objects.filter(state="Сдан")
    paginator = Paginator(projectsList, 20)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    paginator1 = Paginator(completedProjectsList, 20)
    pageNumber1 = request.GET.get('page')
    pageObj1 = paginator1.get_page(pageNumber1)
    return render(request, "projects.html",{"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "project": projectsList, "pageObj": pageObj, "completedProjectsList": completedProjectsList, "messageList": messageList, "msgState": msgState, "pageObj1": pageObj1})

def newProjectForm(request):
    user = User.objects.get(login=request.session['login'])
    if request.method == "GET":
        messageList = list()
        msgState = 1
        messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
        for msg in messages:
            if (msg.messageStatus == 0):
                messageList.append(msg)
        if (len(messageList) == 0):
            msgState = 0
        form = NewProjectForm()
        return render(request, "newProject.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "messageList": messageList, "msgState": msgState, "login": request.session['login']})
    if request.method == "POST":
        messageList = list()
        msgState = 1
        messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
        for msg in messages:
            if (msg.messageStatus == 0):
                messageList.append(msg)
        if (len(messageList) == 0):
            msgState = 0
        form = NewProjectForm(request.POST)
        project = Project()
        project.title = request.POST.get("title")
        project.clientName = request.POST.get("clientName")
        project.dateStart = request.POST.get("dateStart")
        project.dateEnd = request.POST.get("dateEnd")
        project.email = request.POST.get("email")
        project.number = request.POST.get("number")
        project.state = "Принят"
        project.link = request.POST.get("link")
        project.description = request.POST.get("description")
        if "@" in request.POST.get("email"):
            project.save()
            return HttpResponseRedirect("/projects/")
        else:
            errorMsg = "Проверьте, указан ли домен в поле \"E-mail\""
            return render(request, "newProject.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "messageList": messageList, "msgState": msgState, "login": request.session['login'], "errorMsg": errorMsg})

def editProject(request, id):
    if request.session['login'] == "none":
        return HttpResponse('У вас нет доступа к этой странице')
    else:
        try:
            user = User.objects.get(login=request.session['login'])
            messageList = list()
            msgState = 1
            messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
            for msg in messages:
                if (msg.messageStatus == 0):
                    messageList.append(msg)
            if (len(messageList) == 0):
                msgState = 0
            project = Project.objects.get(id=id)
            if request.method == "POST":
                project.title = request.POST.get("title")
                project.dateStart = request.POST.get("dateStart")
                project.dateEnd = request.POST.get("dateEnd")
                project.clientName = request.POST.get("clientName")
                project.email = request.POST.get("email")
                project.number = request.POST.get("number")
                project.link = request.POST.get("link")
                project.description = request.POST.get("description")
                if (project.title != '' and project.dateStart != '' and project.dateEnd != '' and project.clientName != '' and project.email != '' and '@' in request.POST.get("email") and project.number != ''):
                    project.save()
                    tasks = Task.objects.filter(idProject=id)
                    for task in tasks:
                        task.titleProject = project.title
                        task.save()
                else:
                    errorMsg = "Проверьте, все ли поля были заполнены:\n- \"Название проекта\"\n- \"Триггер начала\"\n- \"Триггер окончания\"\n- \"Имя клиента\"\n- \"E-mail клиента\"\n- \"Номер клиента\"\n(проверьте, указан ли домен в поле \"E-mail клиента\")"
                    return render(request, "editProject.html", {"project": project, "name": request.session['name'], "tag": request.session['tag'], "messageList": messageList, "msgState": msgState, "projectTitle": project.title, "errorMsg": errorMsg})
                return HttpResponseRedirect("/projects/")
            else:
                return render(request, "editProject.html", {"project": project, "name": request.session['name'], "tag": request.session['tag'], "messageList": messageList, "msgState": msgState, "projectTitle": project.title})
        except Project.DoesNotExist:
            return HttpResponseNotFound("<h2>Проект не найден</h2>")

def saveEditProjectState(request, id, state):
    try:
            project = Project.objects.get(id=id)
            project.state = state
            project.save()
            return HttpResponseRedirect("/projects/")
    except Project.DoesNotExist:
        return HttpResponseNotFound("<h2>Проект не найден</h2>")

def deleteProject(request, id):
    try:
        project = Project.objects.get(id=id)
        tasks = Task.objects.filter(idProject=id)
        for task in tasks:
            Message.objects.filter(idTask = task.id).delete()
        Task.objects.filter(idProject=id).delete()
        project.delete()
        return HttpResponseRedirect("/projects/")
    except Project.DoesNotExist:
        return HttpResponseNotFound("<h2>Проект не найден</h2>")
#КонецДействияСПроектами

#ДействияСЗадачами
def taskForm(request, id):
    user=User.objects.get(login=request.session['login'])
    messageList = list()
    msgState = 1
    messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
    for msg in messages:
        if (msg.messageStatus == 0):
            messageList.append(msg)
    if (len(messageList) == 0):
        msgState = 0
    userList = User.objects.all()
    taskListInDream = Task.objects.filter(idProject=id, state="В планах")
    taskListAccepted = Task.objects.filter(idProject=id, state="Принята")
    taskListInWork = Task.objects.filter(idProject=id, state="В работе")
    taskListStoped = Task.objects.filter(idProject=id, state="Приостановлена")
    taskListAccompaniment = Task.objects.filter(idProject=id, state="Сопровождение")
    taskListCompleted = Task.objects.filter(idProject=id, state="Сделана")
    taskList = Task.objects.filter(idProject=id)
    project = Project.objects.get(id = id)
    projectTitle = project.title
    return render(request, "tasks.html",
                      {"tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "messageList": messageList, 
                       "msgState": msgState, "taskList": taskList, "id": id, "userList": userList, "projectTitle": projectTitle, "visual": user.visual, 
                       "taskListAccepted": taskListAccepted, "taskListInWork": taskListInWork,"taskListStoped": taskListStoped, "taskListCompleted": taskListCompleted, 
                       "taskListAccompaniment": taskListAccompaniment, "taskListInDream": taskListInDream})

def newTaskForm(request, id):
    user=User.objects.get(login=request.session['login'])
    messageList = list()
    msgState = 1
    messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
    for msg in messages:
        if (msg.messageStatus == 0):
            messageList.append(msg)
    if (len(messageList) == 0):
        msgState = 0
    if request.method == "GET":
        form = NewTaskForm()
        return render(request, "newTask.html", {"form": form, "tag": request.session['tag'],"name": request.session['name'],  "login": request.session['login'], "messageList": messageList, "msgState": msgState,})
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        project = Project.objects.get(id=id)
        user = User.objects.get(name=request.session['name'])
        task = Task()
        task.title = request.POST.get("title")
        task.executorName = request.POST.get("Исполнитель")
        task.dateStart = request.POST.get("dateStart")
        task.dateEnd = request.POST.get("dateEnd")
        task.titleProject = project.title
        task.state = "В планах"
        task.link = request.POST.get("link")
        task.description = request.POST.get("description")
        executor = User.objects.get(name=request.POST.get("Исполнитель"))
        task.idResponsible=user.id
        task.responsibleName = request.session['name']
        task.idExecutor=executor.id
        task.idProject=id
        task.save()
    return HttpResponseRedirect("/projects/tasks/"+str(task.idProject)+"/")

def fallInTask(request, id):
    if request.session['login'] == "none":
        return HttpResponse('У вас нет доступа к этой странице')
    else:
        try:
            errorMsg = ''
            messageList = list()
            userList = User.objects.all()
            user=User.objects.get(login=request.session['login'])
            idUser=user.id
            task = Task.objects.get(id=id)
            messagesChat = Message.objects.filter(idTask = id)
            project = Project.objects.get(id=task.idProject)
            msgState = 1
            messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
            for msg in messages:
                if (task.id == msg.idTask):
                    msg.messageStatus = 1
                    msg.save()
                if (msg.messageStatus == 0):
                    messageList.append(msg)
            if (len(messageList) == 0):
                msgState = 0
            if request.method == "POST":
                if(user.tag == "Администратор"):
                    task.title = request.POST.get("title")
                    task.dateStart = request.POST.get("dateStart")
                    task.dateEnd = request.POST.get("dateEnd")
                    task.titleProject = project.title
                    task.state = request.POST.get("state")
                    task.link = request.POST.get("link")
                    task.description = request.POST.get("description")
                    executor = User.objects.get(id=request.POST.get("executor"))
                    task.executorName = executor.name
                    idUser = executor.id
                    task.idExecutor = executor.id
                    task.idProject = project.id
                    if (task.title != '' and task.description != '' and task.dateStart != '' and task.dateEnd != '' and task.link != ''):
                        task.save()
                        return HttpResponseRedirect("/task/"+str(task.id)+"/")
                    else:
                        errorMsg = "Проверьте, все ли поля были заполнены:\n- \"Задача\"\n- \"Описание\"\n- \"Триггер начала\"\n- \"Триггер окончания\"\n- \"Ссылки\""
                        return render(request, "fallInTask.html", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messagesChat": messagesChat, "userList": userList, "messageList": messageList, "msgState": msgState, "errorMsg": errorMsg})
                else:
                    task.link = request.POST.get("link")
                    task.state = request.POST.get("state")
                    if (task.link != ''):
                        task.save()
                        return HttpResponseRedirect("/task/"+str(task.id)+"/")
                    else:
                        errorMsg = "Проверьте, все ли поля были заполнены:\n- \"Ссылки\""
                        return render(request, "fallInTask.html", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messagesChat": messagesChat, "userList": userList, "messageList": messageList, "msgState": msgState, "errorMsg": errorMsg})
            else:
                return render(request, "fallInTask.html", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messagesChat": messagesChat, "userList": userList, "messageList": messageList, "msgState": msgState, "errorMsg": errorMsg})
        except Task.DoesNotExist:
            return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def saveEditTask(request, id, description, link, state, executorId):
    try:
            task = Task.objects.get(id=id)
            task.description = description
            task.link = link
            task.state = state
            user = User.objects.get(id=executorId)
            task.idExecutor = executorId
            task.executorName = user.name
            task.save()
            return HttpResponseRedirect("/projects/tasks/"+str(task.idProject)+"/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def mainSaveEditTask(request, id, state, executorId):
    try:
        task = Task.objects.get(id=id)
        task.state = state
        user = User.objects.get(id=executorId)
        task.idExecutor = executorId
        task.executorName = user.name
        task.save()
        return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def inTaskEditDateEnd(request, id, dateEnd):
    try:
        if(dateEnd != ""):
            userList = User.objects.all()
            task = Task.objects.get(id=id)
            messages = Message.objects.filter(idTask=task.id)
            user = User.objects.get(login=request.session['login'])
            idUser = user.id
            task.dateEnd = dateEnd
            task.save()
            return HttpResponseRedirect("/task/" + str(task.id) + "/", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messages": messages, "userList": userList})
        else:
            userList = User.objects.all()
            task = Task.objects.get(id=id)
            messages = Message.objects.filter(idTask=task.id)
            user = User.objects.get(login=request.session['login'])
            idUser = user.id
            errorMsg = "Дата окончания не может быть пуста"
            return render(request, "fallInTask.html", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "userList": userList, "messages": messages, "errorMsg": errorMsg})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def inTaskEditLink(request, id, link):
    try:
            userList = User.objects.all()
            task = Task.objects.get(id=id)
            messages = Message.objects.filter(idTask=task.id)
            user = User.objects.get(login=request.session['login'])
            idUser = user.id
            task.link = link
            task.save()
            return HttpResponseRedirect("/task/" + str(task.id) + "/",{"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messages": messages, "userList": userList})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def inTaskEditDescription(request, id, description):
    try:
            userList = User.objects.all()
            task = Task.objects.get(id=id)
            messages = Message.objects.filter(idTask=task.id)
            user = User.objects.get(login=request.session['login'])
            idUser = user.id
            task.description = description
            task.save()
            return HttpResponseRedirect("/task/" + str(task.id) + "/", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messages": messages, "userList": userList})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def inTaskEditExecutor(request, id, executor):
    try:
            userList = User.objects.all()
            task = Task.objects.get(id=id)
            messages = Message.objects.filter(idTask=task.id)
            user = User.objects.get(login=request.session['login'])
            idUser = user.id
            newExecutor = User.objects.get(id=executor)
            task.idExecutor = newExecutor.id
            task.executorName = newExecutor.name
            task.save()
            return HttpResponseRedirect("/task/" + str(task.id) + "/", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messages": messages, "userList": userList})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def inTaskEditState(request, id, state):
    try:
            userList = User.objects.all()
            task = Task.objects.get(id=id)
            messages = Message.objects.filter(idTask=task.id)
            user = User.objects.get(login=request.session['login'])
            idUser = user.id
            task.state = state
            task.save()
            return HttpResponseRedirect("/task/" + str(task.id) + "/", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messages": messages, "userList": userList})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def inTaskEditTitle(request, id, title):
    try:
            userList = User.objects.all()
            task = Task.objects.get(id=id)
            messages = Message.objects.filter(idTask=task.id)
            user = User.objects.get(login=request.session['login'])
            idUser = user.id
            task.title = title
            task.save()
            return HttpResponseRedirect("/task/" + str(task.id) + "/", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "idUser": idUser, "messages": messages, "userList": userList})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def mainUserSaveEditTask(request, id, description, link, state):
    try:
            task = Task.objects.get(id=id)
            task.description = description
            task.link = link
            task.state = state
            task.save()
            return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def tasksUserSaveEditTask(request, id, state, executorId):
    try:
            task = Task.objects.get(id=id)
            executor = User.objects.get(id=executorId)
            task.idExecutor = executorId
            task.executorName = executor.name
            task.state = state
            task.save()
            return HttpResponseRedirect("/projects/tasks/"+ str(task.idProject) + "/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def mainUserSaveEditTask1(request, id, state):
    try:
        task = Task.objects.get(id=id)
        task.state = state
        task.save()
        return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")
    
def tasksSaveEditTask(request, id, state):
    try:
        task = Task.objects.get(id=id)
        task.state = state
        task.save()
        return HttpResponseRedirect("/projects/tasks/"+ str(task.idProject) +"/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def deleteTask(request, id):
    try:
        task = Task.objects.get(id=id)
        Message.objects.filter(idTask = id).delete()
        idProject = task.idProject
        task.delete()
        return HttpResponseRedirect("/projects/tasks/"+str(idProject)+"/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")

def deleteTaskMain(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")
#КонецДействияСЗадачами

#Сообщения
def saveMessage(request, id, idUser, message):
    try:
        messageList = list()
        userList = User.objects.all()
        newMessage = Message()
        task = Task.objects.get(id=id)
        user = User.objects.get(login=request.session['login'])
        newMessage.messageText = message
        date = datetime.now()
        dateWrite = str(date.day) + "." + str(date.month) + "." + str(date.year) + " " + str(date.hour) + ":" + str(date.minute)
        newMessage.date = dateWrite
        newMessage.idUser = user.id
        newMessage.userName = user.name
        newMessage.idTask = id
        if(user.id == task.idExecutor):
            newMessage.idUserRecipient = task.idResponsible
        else:
            newMessage.idUserRecipient = task.idExecutor
        newMessage.messageStatus = 0
        newMessage.save()
        messages = Message.objects.filter(idTask=id)
        msgState = 1
        messagesNotification = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=task.idExecutor)
        for msg in messagesNotification:
            if (msg.messageStatus == 0):
                messageList.append(msg)
        if (len(messageList) == 0):
            msgState = 0
        return HttpResponseRedirect("/task/" + str(task.id) + "/",
                                    {"task": task, "tag": request.session['tag'], "name": request.session['name'],
                                     "login": request.session['login'], "idUser": user.id, "messages": messages,
                                     "userList": userList, "messageList": messageList, "msgState": msgState})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Задача не найдена</h2>")
#КонецСообщения

#Статистика
def statistics(request):
    user = User.objects.get(login=request.session['login'])
    messageList = list()
    msgState = 1
    messages = Message.objects.filter(idUserRecipient=user.id).exclude(idUser=user.id)
    for msg in messages:
        if (msg.messageStatus == 0):
            messageList.append(msg)
    if (len(messageList) == 0):
        msgState = 0
    projects = Project.objects.all()
    projectsAccepted = Project.objects.filter(state="Принят")
    projectsInWork = Project.objects.filter(state="В работе")
    projectsReady = Project.objects.filter(state="Сдан")
    projectsStop = Project.objects.filter(state="Приостановлен")
    taskListProjects = {}
    for project in projects:
        taskListProjects[project.id] = [Task.objects.filter(titleProject=project.title).count(), Task.objects.filter(titleProject=project.title, state="В планах").count(), Task.objects.filter(titleProject=project.title, state="Принята").count(),
                                           Task.objects.filter(titleProject=project.title, state="В работе").count(), Task.objects.filter(titleProject=project.title, state="Сопровождение").count(),
                                           Task.objects.filter(titleProject=project.title, state="Приостановлена").count(), Task.objects.filter(titleProject=project.title, state="Сделана").count()]

    taskCount = Task.objects.all().count()
    taskAcceptedCount = Task.objects.filter(state="Принята").count()
    taskInWorkCount = Task.objects.filter(state="В работе").count()
    taskStopCount= Task.objects.filter(state="Приостановлена").count()
    taskAccompanimentCount = Task.objects.filter(state="Сопровождение").count()
    taskReadyCount = Task.objects.filter(state="Сделана").count()
    return render(request, "statistics.html",
                  {"tag": request.session['tag'],  "name": request.session['name'], "login": request.session['login'],
                   "projects": projects, "projectsAcceptedCount": projectsAccepted.count(), "projectsInWorkCount": projectsInWork.count(),
                   "projectsReadyCount": projectsReady.count(), "projectsStopCount": projectsStop.count(), "taskListProjects": taskListProjects,
                   "projectsCount": projects.count(), "taskCount": taskCount,
                   "taskAcceptedCount": taskAcceptedCount, "taskInWorkCount": taskInWorkCount, "taskStopCount": taskStopCount,
                   "taskAccompanimentCount": taskAccompanimentCount, "taskReadyCount": taskReadyCount, "messageList": messageList, "msgState": msgState})
#КонецСтатистика