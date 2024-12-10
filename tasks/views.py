from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Task, Category
from .forms import TaskForm
from django.core.mail import send_mail

@login_required
def task_list(request):
    user = request.user
    tasks = Task.objects.filter(user=user)

    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    due_date_filter = request.GET.get('due_date')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if due_date_filter:
        tasks = tasks.filter(due_date=due_date_filter)
        
        
    for task in tasks:
        if task.due_date <= timezone.now() and task.status == 'pending':
            task.status = 'due'
            task.save()

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_list.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})



'''
# tasks/views.py

from django.shortcuts import render, redirect
from .models import Task
from django.utils import timezone
from .forms import TaskForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
'''

@login_required
def complete_task(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        if 'yes' in request.POST:
            task.status = 'completed'
        else:
            task.status = 'due'
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/complete_task.html', {'task': task})


from django.shortcuts import render
from django.http import JsonResponse
from .models import Task  # Import your Task model

from django.shortcuts import render
from tasks.models import Task  # Import your Task model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def analytics_data(request):
    user_tasks = Task.objects.filter(user=request.user)
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='completed').count()
    pending_tasks = total_tasks - completed_tasks

    data = {
        "labels": ["Completed Tasks", "Pending Tasks"],
        "data": [completed_tasks, pending_tasks],
    }
    return JsonResponse(data)

