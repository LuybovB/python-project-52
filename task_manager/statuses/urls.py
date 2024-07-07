from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_statuses, name='list_statuses'),
    path('create/', views.create_status, name='create_status'),
    path('<int:pk>/update/', views.update_status, name='update_status'),
    path('<int:pk>/delete/', views.delete_status, name='delete_status'),
]
