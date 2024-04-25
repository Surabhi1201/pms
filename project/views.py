from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from . models import Project, ProjectFile
from task.models import Task


@login_required
def projects(request):
    projects = Project.objects.filter(created_by=request.user)
    tasks_count = {}

    for project in projects:
        tasks = Task.objects.filter(project=project)
        num_tasks = tasks.count()
        tasks_count[project.id] = num_tasks

    return render(request, 'project/projects.html', {
        'projects': projects,
        'tasks_count': tasks_count,
    })


@login_required
def project(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)
    return render(request, 'project/project.html', {
        'project':project,
    })


@login_required
def add_project(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            project = Project.objects.create(name=name, description=description, created_by=request.user)
            return redirect('/projects/')
        else:
            print("Not valid")

    return render(request, 'project/add.html')


@login_required
def edit(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')

        if name:
            project.name = name
            project.description = description
            project.save()

            return redirect('/projects')
    
    return render(request, 'project/edit.html', {
        'project':project,
    })

@login_required
def delete(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)
    project.delete()

    return redirect('/projects/')


@login_required
def files(request, project_id):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    projectfiles = project.files.all

    return render(request, 'project/files.html', {
        'project': project,
        'projectfiles': projectfiles
    })

@login_required
def upload_file(request, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '')
        attachment = request.FILES.get('attachment', '')

        ProjectFile.objects.create(name=name, attachment=attachment, project=project)
        return redirect(f'/projects/{pk}/files/')

    return render(request, 'project/upload_file.html', {
        'project': project,
    })


@login_required
def delete_file(request, project_id, pk):
    project = Project.objects.filter(created_by=request.user).get(pk=project_id)
    projectfile = project.files.get(pk=pk)
    projectfile.delete()

    return redirect(f'/projects/{project_id}/files/')
