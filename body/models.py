from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Role(models.Model):
    USER = "user"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True, verbose_name="Роль")

    class Meta:
        ordering = ["name"]
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name="ФИО", blank=True)
    login = models.CharField(max_length=150, unique=True, blank=True, verbose_name="Логин")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Роль")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.full_name or self.username

    def save(self, *args, **kwargs):
        if not self.login:
            self.login = self.username
        super().save(*args, **kwargs)

    def is_admin(self):
        return bool(self.is_superuser or self.is_staff or (self.role and self.role.name == Role.ADMIN))

    def can_manage_categories(self):
        return self.is_admin()

    def can_view_all_tasks(self):
        return self.is_admin()


class TaskCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория задач"
        verbose_name_plural = "Категории задач"

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_CANCELLED = "cancelled"

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_IN_PROGRESS, "В работе"),
        (STATUS_DONE, "Выполнена"),
        (STATUS_CANCELLED, "Отменена"),
    ]

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Низкий"),
        (PRIORITY_MEDIUM, "Средний"),
        (PRIORITY_HIGH, "Высокий"),
    ]

    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name="Статус")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM, verbose_name="Приоритет")
    due_date = models.DateField(null=True, blank=True, verbose_name="Срок выполнения")
    is_completed = models.BooleanField(default=False, verbose_name="Выполнена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks", verbose_name="Пользователь")
    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name="Категория",
    )

    class Meta:
        ordering = ["is_completed", "due_date", "-created_at"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title

    def is_overdue(self):
        return bool(self.due_date and not self.is_completed and self.due_date < timezone.localdate())

    def get_status_badge_class(self):
        return {
            self.STATUS_NEW: "secondary",
            self.STATUS_IN_PROGRESS: "warning text-dark",
            self.STATUS_DONE: "success",
            self.STATUS_CANCELLED: "danger",
        }.get(self.status, "secondary")

    def get_priority_badge_class(self):
        return {
            self.PRIORITY_LOW: "info text-dark",
            self.PRIORITY_MEDIUM: "primary",
            self.PRIORITY_HIGH: "danger",
        }.get(self.priority, "secondary")

    def sync_completion_state(self):
        self.is_completed = self.status == self.STATUS_DONE

    def save(self, *args, **kwargs):
        self.sync_completion_state()
        super().save(*args, **kwargs)
