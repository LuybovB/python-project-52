"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import IndexView, register, user_list, login_view, logout_view, user_update_view, user_delete_view
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
    path('statuses/<int:pk>/update/', views.update_status, name='update_status'),
    path('statuses/<int:pk>/delete/', views.delete_status, name='delete_status'),
]
