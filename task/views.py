from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . models import Task
from project.models import Project


@login_required
def tasks(request, project_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    tasks = Task.objects.filter(project=project)
    status = {}
    for task in tasks:
        if task.is_done == True:
            status[task.id] = "Done"
        else:
            status[task.id] = "Pending"

    return render(request, 'task/tasks.html', {
        'project':project,
        'tasks':tasks,
        'status':status,
    })

@login_required
def task(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    task = Task.objects.filter(project=project).get(pk=pk)

    if request.GET.get('is_done', '') == 'yes':
        task.is_done = True
        task.save()

    return render(request, 'task/task.html', {
        'project':project,
        'task':task
    })

@login_required
def add(request, project_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            Task.objects.create(project=project, name=name, description=description, created_by=request.user)
            return redirect(f'/projects/{project_id}/tasks/')
    return render(request, 'task/add.html')

@login_required
def edit(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    task = Task.objects.filter(project=project).get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        descripton = request.POST.get('description', '')

        if name:
            task.name = name
            task.description = descripton
            task.save()

            return redirect(f'/projects/{project_id}/tasks/{pk}/')

    return render(request, 'task/edit.html', {
        'project' : project,
        'task' : task,
    })

@login_required
def delete(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    task = Task.objects.filter(project=project).get(pk=pk)
    task.delete()

    return redirect(f'/projects/{project_id}/tasks/')