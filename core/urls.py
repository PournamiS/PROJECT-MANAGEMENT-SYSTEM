from django.urls import path
from . import views

urlpatterns = [
    path('',              views.login_view,  name='login'),
    path('login/',        views.login_view,  name='login'),
    path('logout/',       views.logout_view, name='logout'),
    path('dashboard/',    views.dashboard,   name='dashboard'),

    # Users
    path('users/',                   views.user_list,   name='user_list'),
    path('users/create/',            views.user_create, name='user_create'),
    path('users/<int:pk>/edit/',     views.user_edit,   name='user_edit'),
    path('users/<int:pk>/delete/',   views.user_delete, name='user_delete'),

    # Projects
    path('projects/',                  views.project_list,   name='project_list'),
    path('projects/create/',           views.project_create, name='project_create'),
    path('projects/<int:pk>/',         views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/',    views.project_edit,   name='project_edit'),
    path('projects/<int:pk>/delete/',  views.project_delete, name='project_delete'),

    # Tasks
    path('tasks/',                 views.task_list,   name='task_list'),
    path('tasks/create/',          views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/',   views.task_edit,   name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
