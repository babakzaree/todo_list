from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from todo.models import Task
from todo.forms import TaskForm


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'todo/task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})


def task_delete(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('task_list')
    else:
        return HttpResponseNotAllowed(['POST'])


def complete_task(request, task_id):
    # Retrieve the task object
    task = get_object_or_404(Task, pk=task_id)

    # Mark the task as complete
    task.completed = True
    task.save()

    # Redirect to the task list page
    return redirect('task_list')
