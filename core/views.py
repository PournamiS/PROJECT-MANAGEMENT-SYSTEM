from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import User, Project, Task
from .forms import UserCreateForm, UserEditForm, ProjectForm, TaskForm, TaskStatusForm
from .decorators import admin_required, login_required_custom


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required_custom
def dashboard(request):
    user = request.user
    if user.is_admin():
        total_users    = User.objects.count()
        total_projects = Project.objects.count()
        total_tasks    = Task.objects.count()
        pending        = Task.objects.filter(status='pending').count()
        in_progress    = Task.objects.filter(status='in_progress').count()
        completed      = Task.objects.filter(status='completed').count()
        recent_projects = Project.objects.order_by('-created_at')[:5]
        recent_tasks    = Task.objects.order_by('-created_at')[:5]
    else:
        total_users    = None
        total_projects = user.projects.count()
        total_tasks    = user.tasks.count()
        pending        = user.tasks.filter(status='pending').count()
        in_progress    = user.tasks.filter(status='in_progress').count()
        completed      = user.tasks.filter(status='completed').count()
        recent_projects = user.projects.order_by('-created_at')[:5]
        recent_tasks    = user.tasks.order_by('-created_at')[:5]

    context = {
        'total_users':    total_users,
        'total_projects': total_projects,
        'total_tasks':    total_tasks,
        'pending':        pending,
        'in_progress':    in_progress,
        'completed':      completed,
        'recent_projects': recent_projects,
        'recent_tasks':    recent_tasks,
    }
    return render(request, 'dashboard/dashboard.html', context)


# ── Users ─────────────────────────────────────────────────────────────────────

@admin_required
def user_list(request):
    query       = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    users = User.objects.all().order_by('username')
    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))
    if role_filter:
        users = users.filter(role=role_filter)
    paginator = Paginator(users, 10)
    users = paginator.get_page(request.GET.get('page'))
    return render(request, 'users/list.html', {
        'users': users, 'query': query, 'role_filter': role_filter
    })


@admin_required
def user_create(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User created successfully.')
        return redirect('user_list')
    return render(request, 'users/form.html', {'form': form, 'title': 'Add User'})


@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User updated successfully.')
        return redirect('user_list')
    return render(request, 'users/form.html', {'form': form, 'title': 'Edit User'})


@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted.')
        return redirect('user_list')
    return render(request, 'users/confirm_delete.html', {'object': user, 'type': 'User'})


# ── Projects ──────────────────────────────────────────────────────────────────

@login_required_custom
def project_list(request):
    query = request.GET.get('q', '')
    user  = request.user
    projects = Project.objects.all() if user.is_admin() else user.projects.all()
    if query:
        projects = projects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    projects = projects.order_by('-created_at')
    paginator = Paginator(projects, 8)
    projects = paginator.get_page(request.GET.get('page'))
    return render(request, 'projects/list.html', {'projects': projects, 'query': query})


@login_required_custom
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not request.user.is_admin() and request.user not in project.members.all():
        messages.error(request, 'Access denied.')
        return redirect('project_list')
    tasks         = project.tasks.all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    return render(request, 'projects/detail.html', {
        'project': project, 'tasks': tasks, 'status_filter': status_filter
    })


@admin_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        project = form.save(commit=False)
        project.created_by = request.user
        project.save()
        form.save_m2m()
        messages.success(request, 'Project created.')
        return redirect('project_list')
    return render(request, 'projects/form.html', {'form': form, 'title': 'New Project'})


@admin_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Project updated.')
        return redirect('project_list')
    return render(request, 'projects/form.html', {'form': form, 'title': 'Edit Project'})


@admin_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('project_list')
    return render(request, 'users/confirm_delete.html', {'object': project, 'type': 'Project'})


# ── Tasks ─────────────────────────────────────────────────────────────────────

@login_required_custom
def task_list(request):
    user          = request.user
    query         = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    tasks = Task.objects.all() if user.is_admin() else user.tasks.all()
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    tasks = tasks.order_by('-created_at')
    paginator = Paginator(tasks, 10)
    tasks = paginator.get_page(request.GET.get('page'))
    return render(request, 'tasks/list.html', {
        'tasks': tasks, 'query': query, 'status_filter': status_filter
    })


@admin_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task created.')
        return redirect('task_list')
    return render(request, 'tasks/form.html', {'form': form, 'title': 'New Task'})


@login_required_custom
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    if not user.is_admin() and task.assigned_to != user:
        messages.error(request, 'Access denied.')
        return redirect('task_list')
    form_class = TaskForm if user.is_admin() else TaskStatusForm
    form = form_class(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task updated.')
        return redirect('task_list')
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Edit Task', 'task': task})


@admin_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted.')
        return redirect('task_list')
    return render(request, 'users/confirm_delete.html', {'object': task, 'type': 'Task'})
