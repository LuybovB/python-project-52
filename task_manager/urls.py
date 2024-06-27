from django.contrib import admin
from django.urls import path
from .views import (IndexView, register, user_list,
                    login_view, logout_view,
                    user_update_view, user_delete_view)
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='root'),
    path('users/create/', register, name='register'),
    path('users/', user_list, name='user-list'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/<int:pk>/update/', user_update_view, name='user_update'),
    path('users/<int:pk>/delete/', user_delete_view, name='user_delete'),
    path('users/<int:pk>/delete/', user_delete_view, name='user_delete'),
    path('statuses/', views.list_statuses, name='list_statuses'),
    path('require_login/', views.require_login, name='require_login'),
    path('statuses/create/', views.create_status, name='create_status'),
    path('statuses/<int:pk>/update/', views.update_status,
         name='update_status'),
    path('statuses/<int:pk>/delete/', views.delete_status,
         name='delete_status'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('labels/', views.labels_list, name='labels-list'),
    path('labels/create/', views.label_create, name='label_create'),
    path('labels/<int:pk>/edit/', views.label_update, name='label_update'),
    path('labels/<int:pk>/delete/', views.label_delete, name='label_delete'),
]
