from django.urls import path
from .views import (
    task_list,
    task_create,
    task_update,
    task_delete,
    task_detail
)

app_name = 'tasks'

urlpatterns = [
    path('', task_list, name='list'),
    path('create/', task_create, name='create'),
    path('<int:pk>/', task_detail, name='detail'),
    path('<int:pk>/update/', task_update, name='update'),
    path('<int:pk>/delete/', task_delete, name='delete'),
]
