from django import forms
from django.forms import HiddenInput
from .models import User, Tag, Project

class RegForm(forms.Form):
    login = forms.CharField(max_length=20, label="Логин", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите логин пользователя', 'class': 'login'}))
    password = forms.CharField(max_length=150, min_length=6, label="Пароль", required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль пользователя', 'class': 'password'}))
    name = forms.CharField(max_length=100, label="Ф.И.О", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите Ф.И.О пользователя', 'class': 'name'}))
    email = forms.EmailField(label="E-mail", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите E-mail пользователя', 'class': 'email'}))
    number = forms.CharField(max_length=11, min_length=6, label="Номер телефона", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона пользователя', 'class': 'number'}))
    birthday = forms.CharField(max_length=10, label="День рождения", widget=forms.TextInput(attrs={'placeholder': 'Введите дату рождения пользователя', 'class': 'date'}))

class NewProjectForm(forms.Form):
    title = forms.CharField(max_length=150, label="Название проекта", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите название проекта', 'class': 'title'}))
    description = forms.CharField(label="Описание", required=True, widget=forms.Textarea(attrs={'placeholder': 'Введите описание проекта', 'class': 'description'}))
    clientName = forms.CharField(max_length=100, label="Имя клиента", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите имя клиента', 'class': 'clientName'}))
    dateStart = forms.CharField(max_length=10, label="Триггер начала", widget=forms.TextInput(attrs={'placeholder': 'Введите триггер начала проекта', 'class': 'dateStart'}))
    dateEnd = forms.CharField(max_length=10, label="Триггер окончания", widget=forms.TextInput(attrs={'placeholder': 'Введите триггер окончания проекта', 'class': 'dateEnd'}))
    email = forms.EmailField(label="E-mail",  required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите E-mail клиента', 'class': 'email'}))
    number = forms.CharField(max_length=11, label="Номер телефона", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона клиента', 'class': 'number'}))
    link = forms.CharField(label="Ссылки", required=True, widget=forms.Textarea(attrs={'placeholder': 'Введите ссылки к проекту', 'class': 'link'}))

class NewTaskForm(forms.Form):
    title = forms.CharField(max_length=150, label="Название задачи", required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите название задачи', 'class': 'title'}))
    description = forms.CharField(max_length=1000, label="Описание", required=True, widget=forms.Textarea(attrs={'placeholder': 'Введите описание задачи','class': 'description'}))
    Исполнитель = forms.ModelChoiceField(User.objects.order_by().values_list('name', flat=True).distinct(), widget=forms.Select(attrs={'placeholder': 'Выберите исполнителя задачи', 'class': 'executor'}))
    dateStart = forms.CharField(max_length=10, label="Триггер начала", widget=forms.TextInput(attrs={'placeholder': 'Введите триггер начала задачи', 'class': 'dateStart'}))
    dateEnd = forms.CharField(max_length=10, label="Триггер окончания", widget=forms.TextInput(attrs={'placeholder': 'Введите триггер окончания задачи', 'class': 'dateEnd'}))
    link = forms.CharField(max_length=1000, label="Ссылки", required=True, widget=forms.Textarea(attrs={'placeholder': 'Введите ссылки к задаче', 'class': 'link'}))

class MainSpaceForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Тут вы можете оставлять свои заметки, главное не забывать нажимать кнопку "Сохранить"'}))
