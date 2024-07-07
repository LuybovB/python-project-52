from django.contrib import admin
from django.urls import path, include
from .views import (IndexView, register, user_list,
                    login_view, logout_view,
                    user_update_view, user_delete_view)

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
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
]
