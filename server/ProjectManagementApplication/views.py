from datetime import datetime
from passlib.hash import pbkdf2_sha256
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse
from .models import User, Tag, Project, Task
from .form import RegForm, NewProjectForm, NewTaskForm, MainSpaceForm
from django.core.paginator import *
from sys import getdefaultencoding

def index(request):
    try:
        userList = User.objects.all()
        name = request.session['name']
        login = request.session['login']
        tag = request.session['tag']
        form = MainSpaceForm()
        user = User.objects.get(login=request.session['login'])
        comment = user.comment
        if request.method == "POST":
            user.comment = request.POST.get("comment")
            user.save()
            return HttpResponseRedirect("/")
        taskList = Task.objects.filter(idExecutor=user.id)
        paginator = Paginator(taskList, 20)
        pageNumber = request.GET.get('page')
        pageObj = paginator.get_page(pageNumber)
        dateNow = datetime.now()
        dateNow = dateNow.strftime("%d.%m.%Y")
        upcomingTasksList = Task.objects.filter(dateEnd=str(dateNow)) & Task.objects.filter(idExecutor=user.id)
        paginator1 = Paginator(upcomingTasksList, 5)
        pageNumber1 = request.GET.get('page')
        pageObj1 = paginator1.get_page(pageNumber1)
    except:
        request.session['name'] = 'Неавторизованный пользователь'
        request.session['login'] = "none"
        request.session['tag'] = "guest"
        tag = request.session['tag']
        form = None
        login = request.session['login']
        name = request.session['name']
        comment=''
        upcomingTasksList=None
        taskList=None
        pageObj1=None
        pageObj = None
    return render(request, "index.html", {"tag": tag, "name": name, "login": login, "form": form, "comment": comment, "tasks": taskList, "pageObj": pageObj, "userList": userList, "upcomingTasks": upcomingTasksList, "pageObj1": pageObj1})

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
            password = pbkdf2_sha256.encrypt(request.POST.get("password"), rounds=12000, salt_size=30)
            user.name = request.POST.get("name")
            user.tag = "Администратор"
            users = User.objects.all()
            for i in users:
                if str(i.login) == request.POST.get("login"):
                    j = 0
                    break
            if (user.login != '' and password != '' and user.name != '' and j == 1):
                user.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
                user.save()
                return HttpResponseRedirect("/personalArea/")
            else:
                return HttpResponse(
                    "Выбранный вами логин уже используется или вы допустили другую ошибку при создании аккаунта")
    return render(request, "registrationForAdmin.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login']})

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
            user.tag = "none"
            users = User.objects.all()
            for i in users:
                if str(i.login) == request.POST.get("login"):
                    j=0
                    break
            if (user.login != '' and password != '' and user.name != '' and j == 1):
                user.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
                user.save()
                return HttpResponseRedirect("/personalArea/")
            else:
                return HttpResponse("Выбранный вами логин уже используется или вы допустили другую ошибку при создании аккаунта")
    return render(request, "registration.html", {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "form": form})

def validate_login(request):
    login = request.GET.get('login', None)
    response = {
        'is_taken': User.objects.filter(login=login).exists()
    }
    return JsonResponse(response)

def login(request):
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
        return render(request, "login.html", {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login']})

def editUser(request):
    if request.session['login'] == "none":
        return HttpResponse('У вас нет доступа к этой странице')
    else:
        try:
            tagList = Tag.objects.all()
            paginator = Paginator(tagList, 20)
            pageNumber = request.GET.get('page')
            pageObj = paginator.get_page(pageNumber)
            user = User.objects.get(login=request.session['login'])
            if request.POST:
                if 'tag' in request.POST:
                    tag = Tag()
                    tag.name = request.POST.get("tagName")
                    tag.save()
                    return HttpResponseRedirect("/personalArea/")
                elif 'user' in request.POST:
                    password = request.POST.get("password")
                    if (request.POST.get("name") != '' and request.POST.get("login") != '' and password != ''):
                            user.name = request.POST.get("name")
                            user.login = request.POST.get("login")
                            user.number = request.POST.get("number")
                            user.password = pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=30)
                            user.save()
                            request.session['name'] = user.name
                            request.session['login'] = user.login
                    elif (request.POST.get("name") != '' and request.POST.get("login") != '' and password == ''):
                            user.name = request.POST.get("name")
                            user.login = request.POST.get("login")
                            user.number = request.POST.get("number")
                            user.save()
                            request.session['name'] = user.name
                            request.session['login'] = user.login
                    else:
                        return HttpResponse('Введенны некорректные данные')
                return HttpResponseRedirect("/")
            else:
                return render(request, "personalArea.html", {"user": user, "tagList": tagList, "pageObj": pageObj, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login']})
        except User.DoesNotExist:
            return HttpResponseNotFound("<h2>User not found</h2>")

def logout(request):
    try:
        request.session['name'] = 'Неавторизованный пользователь'
        request.session['login'] = "none"
        request.session['tag'] = "guest"
    except KeyError:
        pass
    return HttpResponseRedirect("/")

# изменение данных в бд
def tagUsers(request):
    objects = list(Tag.objects.all())
    usersList = User.objects.exclude(tag="Администратор")
    paginator = Paginator(usersList, 10)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)
    return render(request, "tagUsers.html",
                      {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "usersList": usersList, "pageObj": pageObj, "tagList": objects})

def saveEdit(request, id, tag):
    try:
        user = User.objects.get(id=id)
        user.tag = tag
        if (user.tag != ''):
            user.save()
            return HttpResponseRedirect("/tagUsers/")
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")

def saveEditProject(request, id, comment, link, state):
    try:
            project = Project.objects.get(id=id)
            project.comment = comment
            project.link = link
            project.state = state
            project.save()
            return HttpResponseRedirect("/projects/")
    except Project.DoesNotExist:
        return HttpResponseNotFound("<h2>Project not found</h2>")

def saveEditTask(request, id, comment, link, state, executorId):
    try:
            task = Task.objects.get(id=id)
            task.comment = comment
            task.link = link
            task.state = state
            user = User.objects.get(id=executorId)
            task.idExecutor = executorId
            task.executor = user.name
            task.save()
            return HttpResponseRedirect("/projects/tasks/"+str(task.idProject)+"/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")

def mainSaveEditTask(request, id, comment, link, state, executorId):
    try:
            task = Task.objects.get(id=id)
            task.comment = comment
            task.link = link
            task.state = state
            user = User.objects.get(id=executorId)
            task.idExecutor = executorId
            task.executor = user.name
            task.save()
            return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")

def mainUserSaveEditTask(request, id, comment, link, state):
    try:
            task = Task.objects.get(id=id)
            task.comment = comment
            task.link = link
            task.state = state
            task.save()
            return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")

def delete(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return HttpResponseRedirect("/tagUsers/")
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")

def deleteProject(request, id):
    try:
        project = Project.objects.get(id=id)
        Task.objects.filter(idProject=id).delete()
        project.delete()
        return HttpResponseRedirect("/projects/")
    except Project.DoesNotExist:
        return HttpResponseNotFound("<h2>Project not found</h2>")

def deleteTask(request, id):
    try:
        task = Task.objects.get(id=id)
        idProject = task.idProject
        task.delete()
        return HttpResponseRedirect("/projects/tasks/"+str(idProject)+"/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")

def deleteTaskMain(request, id):
    try:
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")

def deleteTag(request, id):
    try:
        tag = Tag.objects.get(id=id)
        tag.delete()
        return HttpResponseRedirect("/personalArea/")
    except Tag.DoesNotExist:
        return HttpResponseNotFound("<h2>Tag not found</h2>")

def projectsForm(request):
    projectsList = Project.objects.exclude(state="Сдан")
    completedProjectsList = Project.objects.filter(state="Сдан")
    paginator = Paginator(projectsList, 20)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    paginator1 = Paginator(completedProjectsList, 20)
    pageNumber1 = request.GET.get('page')
    pageObj1 = paginator1.get_page(pageNumber1)
    return render(request, "projects.html",
                      {"tag": request.session['tag'], "name": request.session['name'], "login": request.session['login'], "project": projectsList, "pageObj": pageObj, "completedProjectsList": completedProjectsList, "pageObj1": pageObj1})

def newProjectForm(request):
    if request.method == "GET":
        form = NewProjectForm()
        return render(request, "newProject.html", {"form": form, "tag": request.session['tag'], "name": request.session['name'], "login": request.session['login']})
    if request.method == "POST":
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
        project.comment = request.POST.get("comment")
        project.save()
    return HttpResponseRedirect("/projects/")

def editProject(request, id):
    if request.session['login'] == "none":
        return HttpResponse('У вас нет доступа к этой странице')
    else:
        try:
            project = Project.objects.get(id=id)
            if request.method == "POST":
                project.title = request.POST.get("title")
                project.dateStart = request.POST.get("dateStart")
                project.dateEnd = request.POST.get("dateEnd")
                project.clientName = request.POST.get("clientName")
                project.email = request.POST.get("email")
                project.number = request.POST.get("number")
                project.link = request.POST.get("link")
                project.comment = request.POST.get("comment")
                if (project.title != '' and project.dateStart != '' and project.dateEnd != '' and project.clientName != '' and project.email != '' and project.number != '' and project.state != ''):
                    project.save()
                else:
                    return HttpResponse('Введенны некорректные данные')
                return HttpResponseRedirect("/projects/")
            else:
                return render(request, "editProject.html", {"project": project, "name": request.session['name'], "tag": request.session['tag'], "title": project.title})
        except Project.DoesNotExist:
            return HttpResponseNotFound("<h2>Проект не найден</h2>")

def taskForm(request, id):
    userList = User.objects.all()
    taskList = Task.objects.filter(idProject=id) & Task.objects.exclude(state="Сделана")
    completedTasksList = Task.objects.filter(idProject=id) & Task.objects.filter(state="Сделана")
    paginator = Paginator(taskList, 20)
    pageNumber = request.GET.get('page')
    pageObj = paginator.get_page(pageNumber)

    paginator1 = Paginator(completedTasksList, 20)
    pageNumber1 = request.GET.get('page')
    pageObj1 = paginator1.get_page(pageNumber1)
    return render(request, "tasks.html",
                      {"tag": request.session['tag'],"name": request.session['name'], "login": request.session['login'], "tasks": taskList, "id": id, "pageObj": pageObj, "userList": userList, "completedTasksList": completedTasksList, "pageObj1": pageObj1})

def newTaskForm(request, id):
    if request.method == "GET":
        form = NewTaskForm()
        return render(request, "newTask.html", {"form": form, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login']})
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        project = Project.objects.get(id=id)
        task = Task()
        task.title = request.POST.get("title")
        task.executor = request.POST.get("Исполнитель")
        task.dateStart = request.POST.get("dateStart")
        task.dateEnd = request.POST.get("dateEnd")
        task.titleProject = project.title
        task.state = "Принята"
        task.link = request.POST.get("link")
        task.comment = request.POST.get("comment")
        executor = User.objects.get(name=request.POST.get("Исполнитель"))
        task.responsible = request.session['name']
        task.idExecutor=executor.id
        task.idProject=id
        task.save()
    return HttpResponseRedirect("/tasks/")

def editTask(request, id):
    if request.session['login'] == "none":
        return HttpResponse('У вас нет доступа к этой странице')
    else:
        try:
            task = Task.objects.get(id=id)
            project = Project.objects.get(id=task.idProject)
            if request.method == "POST":
                task.title = request.POST.get("title")
                task.dateStart = request.POST.get("dateStart")
                task.dateEnd = request.POST.get("dateEnd")
                task.titleProject = project.title
                task.state = "Принята"
                task.link = request.POST.get("link")
                task.comment = request.POST.get("comment")
                executor = User.objects.get(id=task.idExecutor)
                task.executor = executor.name
                task.idExecutor = executor.id
                task.idProject = project.id
                task.save()
                if (task.title != '' and task.dateStart != '' and task.dateEnd != '' and task.executor != ''):
                    task.save()
                else:
                    return HttpResponse('Введенны некорректные данные')
                return HttpResponseRedirect("/projects/tasks/"+str(task.idProject)+"/")
            else:
                return render(request, "editTask.html", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login']})
        except Task.DoesNotExist:
            return HttpResponseNotFound("<h2>Задача не найден</h2>")

def editTaskMain(request, id):
    if request.session['login'] == "none":
        return HttpResponse('У вас нет доступа к этой странице')
    else:
        try:
            task = Task.objects.get(id=id)
            project = Project.objects.get(id=task.idProject)
            if request.method == "POST":
                task.title = request.POST.get("title")
                task.dateStart = request.POST.get("dateStart")
                task.dateEnd = request.POST.get("dateEnd")
                task.titleProject = project.title
                task.state = "Принята"
                task.link = request.POST.get("link")
                task.comment = request.POST.get("comment")
                executor = User.objects.get(id=task.idExecutor)
                task.executor = executor.name
                task.idExecutor = executor.id
                task.idProject = project.id
                task.save()
                if (task.title != '' and task.dateStart != '' and task.dateEnd != '' and task.executor != ''):
                    task.save()
                else:
                    return HttpResponse('Введенны некорректные данные')
                return HttpResponseRedirect("/")
            else:
                return render(request, "editTask.html", {"task": task, "tag": request.session['tag'],"name": request.session['name'], "login": request.session['login']})
        except Task.DoesNotExist:
            return HttpResponseNotFound("<h2>Задача не найден</h2>")