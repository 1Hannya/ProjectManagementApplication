from django import forms
from django.forms import HiddenInput
from .models import User, Tag, Project

class RegForm(forms.Form):
    login = forms.CharField(max_length=20, label="Логин", required=True, widget=forms.TextInput(attrs={'class': 'login'}))
    password = forms.CharField(max_length=150, min_length=6, label="Пароль", required=True, widget=forms.PasswordInput)
    name = forms.CharField(max_length=100, label="Ф.И.О", required=True, widget=forms.TextInput(attrs={'class': 'name'}))
    email = forms.EmailField(label="E-mail", required=True, widget=forms.TextInput(attrs={'class': 'email'}))
    number = forms.CharField(max_length=11, min_length=6, label="Номер телефона", required=True, widget=forms.TextInput(attrs={'class': 'number'}))
    birthday = forms.CharField(max_length=10, label="День рождения")

class NewProjectForm(forms.Form):
    title = forms.CharField(max_length=150, label="Название проекта", required=True, widget=forms.TextInput(attrs={'class': 'title'}))
    clientName = forms.CharField(max_length=100, label="Имя клиента", required=True, widget=forms.TextInput(attrs={'class': 'clientName'}))
    dateStart = forms.CharField(max_length=10, label="Дата начала")
    dateEnd = forms.CharField(max_length=10, label="Дата окончания")
    email = forms.EmailField(label="E-mail", required=True, widget=forms.TextInput(attrs={'class': 'email'}))
    number = forms.CharField(max_length=11, label="Номер телефона", required=True, widget=forms.TextInput(attrs={'class': 'number'}))
    link = forms.CharField(label="Ссылки", required=True, widget=forms.Textarea)
    comment = forms.CharField(label="Комментарий", required=True, widget=forms.Textarea)

class NewTaskForm(forms.Form):
    title = forms.CharField(max_length=150, label="Название задачи", required=True, widget=forms.TextInput(attrs={'class': 'title'}))
    Исполнитель = forms.ModelChoiceField(User.objects.order_by().values_list('name', flat=True).distinct())
    dateStart = forms.CharField(max_length=10, label="Дата начала")
    dateEnd = forms.CharField(max_length=10, label="Дата окончания")
    link = forms.CharField(max_length=1000, label="Ссылки", required=True, widget=forms.Textarea)
    comment = forms.CharField(max_length=1000, label="Комментарий", required=True, widget=forms.Textarea)

class MainSpaceForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
