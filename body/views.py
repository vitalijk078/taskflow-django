from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm, TaskCategoryForm, TaskForm
from .models import Role, Task, TaskCategory, User


def root_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    return redirect("login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("task_list")
    return render(request, "store/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        role, _ = Role.objects.get_or_create(name=Role.USER)
        user.role = role
        user.save()
        login(request, user)
        messages.success(request, "Регистрация прошла успешно.")
        return redirect("task_list")
    return render(request, "store/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def task_list(request):
    tasks = Task.objects.select_related("category", "user")
    categories = TaskCategory.objects.all()

    if not request.user.can_view_all_tasks():
        tasks = tasks.filter(user=request.user)

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    priority = request.GET.get("priority", "").strip()
    category_id = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "due_date").strip()

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if status:
        tasks = tasks.filter(status=status)
    if priority:
        tasks = tasks.filter(priority=priority)
    if category_id:
        tasks = tasks.filter(category_id=category_id)

    order_map = {
        "due_date": ["due_date", "-created_at"],
        "created_at": ["-created_at"],
        "priority": ["priority", "due_date"],
        "title": ["title"],
    }
    tasks = tasks.order_by(*order_map.get(sort, ["due_date", "-created_at"]))

    task_list_for_stats = list(tasks)
    stats = {
        "total": len(task_list_for_stats),
        "in_progress": sum(1 for task in task_list_for_stats if task.status == Task.STATUS_IN_PROGRESS),
        "done": sum(1 for task in task_list_for_stats if task.status == Task.STATUS_DONE),
        "overdue": sum(1 for task in task_list_for_stats if task.is_overdue()),
    }

    context = {
        "tasks": task_list_for_stats,
        "stats": stats,
        "categories": categories,
        "query": query,
        "selected_status": status,
        "selected_priority": priority,
        "selected_category": category_id,
        "sort": sort,
        "status_choices": Task.STATUS_CHOICES,
        "priority_choices": Task.PRIORITY_CHOICES,
    }
    return render(request, "store/task_list.html", context)


@login_required
def task_add(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, "Задача успешно создана.")
        return redirect("task_list")
    return render(request, "store/task_form.html", {"form": form, "title": "Создать задачу", "is_edit": False})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.user != request.user and not request.user.can_view_all_tasks():
        messages.error(request, "Доступ запрещён.")
        return redirect("task_list")

    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Задача «{task.title}» обновлена.")
        return redirect("task_list")
    return render(request, "store/task_form.html", {"form": form, "title": f"Редактировать: {task.title}", "task": task, "is_edit": True})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.user != request.user and not request.user.can_view_all_tasks():
        messages.error(request, "Доступ запрещён.")
        return redirect("task_list")

    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f"Задача «{title}» удалена.")
        return redirect("task_list")
    return render(request, "store/task_confirm_delete.html", {"task": task})


@login_required
@require_POST
def task_toggle_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.user != request.user and not request.user.can_view_all_tasks():
        messages.error(request, "Доступ запрещён.")
        return redirect("task_list")

    if task.status == Task.STATUS_DONE:
        task.status = Task.STATUS_IN_PROGRESS
    else:
        task.status = Task.STATUS_DONE
    task.save()
    messages.success(request, "Статус задачи обновлен.")
    return redirect("task_list")


@login_required
def category_list(request):
    if not request.user.can_manage_categories():
        messages.error(request, "Доступ к категориям есть только у администратора.")
        return redirect("task_list")
    categories = TaskCategory.objects.order_by("name")
    return render(request, "store/category_list.html", {"categories": categories})


@login_required
def category_add(request):
    if not request.user.can_manage_categories():
        messages.error(request, "Доступ запрещён.")
        return redirect("task_list")

    form = TaskCategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Категория добавлена.")
        return redirect("category_list")
    return render(request, "store/category_form.html", {"form": form, "title": "Добавить категорию", "is_edit": False})


@login_required
def category_edit(request, pk):
    if not request.user.can_manage_categories():
        messages.error(request, "Доступ запрещён.")
        return redirect("task_list")

    category = get_object_or_404(TaskCategory, pk=pk)
    form = TaskCategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Категория «{category.name}» обновлена.")
        return redirect("category_list")
    return render(request, "store/category_form.html", {"form": form, "title": f"Редактировать: {category.name}", "is_edit": True, "category": category})


@login_required
def category_delete(request, pk):
    if not request.user.can_manage_categories():
        messages.error(request, "Доступ запрещён.")
        return redirect("task_list")

    category = get_object_or_404(TaskCategory, pk=pk)
    if request.method == "POST":
        name = category.name
        category.delete()
        messages.success(request, f"Категория «{name}» удалена.")
        return redirect("category_list")
    return render(request, "store/category_confirm_delete.html", {"category": category})


def guest_login_view(request):
    role, _ = Role.objects.get_or_create(name=Role.USER)
    guest_user, created = User.objects.get_or_create(
        username="guest",
        defaults={"full_name": "Гость", "is_active": True, "role": role, "login": "guest"},
    )
    if created:
        guest_user.set_unusable_password()
        guest_user.save()

    login(request, guest_user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("task_list")
