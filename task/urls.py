from django.urls import path

from . import views

app_name = 'task'

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('add/', views.add, name='add'),
    path('<uuid:pk>/', views.task, name='task'),
    path('<uuid:pk>/edit/', views.edit, name='edit'),
    path('<uuid:pk>/delete/', views.delete, name='delete'),

]