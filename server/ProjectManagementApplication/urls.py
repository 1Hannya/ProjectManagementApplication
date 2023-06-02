from django.urls import path
from .views import *
import urllib.parse

urlpatterns = [
    path("", index),
    path("registration/", registration, name = "registration"),
    path("registrationForAdmin/", registrationForAdmin, name = "registrationForAdmin"),
    path("validate_login/", validate_login, name="validate_login"),
    path("login/", login),
    path("personalArea/", editUser),
    path("tagUsers/", tagUsers),
    path("saveEdit/<int:id>/<str:tag>/", saveEdit),
    path("saveEditTask/<int:id>/<str:comment>/<path:link>/<str:state>/<int:executorId>/", saveEditTask),
    path("saveEditProject/<int:id>/<str:comment>/<path:link>/<str:state>/", saveEditProject),
    path("mainSaveEditTask/<int:id>/<str:comment>/<path:link>/<str:state>/<int:executorId>/", mainSaveEditTask),
    path("mainUserSaveEditTask/<int:id>/<str:comment>/<path:link>/<str:state>/", mainUserSaveEditTask),
    path("delete/<int:id>/", delete),
    path("projects/deleteProject/<int:id>/", deleteProject),
    path("projects/tasks/deleteTask/<int:id>/", deleteTask),
    path("deleteTaskMain/<int:id>/", deleteTaskMain),
    path("logout/", logout),
    path("projects/", projectsForm),
    path("projects/newProjectForm/", newProjectForm, name = "newProjectForm"),
    path("projects/editProject/<int:id>/", editProject),
    path("projects/newTask/<int:id>/", newTaskForm, name = "newTaskForm"),
    path("projects/tasks/<int:id>/", taskForm),
    path("editTaskMain/<int:id>/", editTaskMain),
    path("projects/tasks/editTask/<int:id>/", editTask),
    path("personalArea/deleteTag/<int:id>/", deleteTag),
]