from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Task, TaskCategory, User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите логин", "autofocus": True}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        label="ФИО",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Иванов Иван Иванович"}),
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}),
    )
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Придумайте логин"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Минимум 8 символов"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("full_name", "email", "username")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get("full_name", "")
        user.email = self.cleaned_data.get("email", "")
        user.login = self.cleaned_data.get("username", "")
        if commit:
            user.save()
        return user


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        label="Срок выполнения",
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например, подготовить отчет"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Кратко опишите задачу"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "title": "Название задачи",
            "description": "Описание",
            "status": "Статус",
            "priority": "Приоритет",
            "category": "Категория",
        }


class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Учеба / Работа / Личное"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Необязательно"}),
        }
        labels = {
            "name": "Название категории",
            "description": "Описание",
        }
