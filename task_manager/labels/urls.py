from django.urls import path
from . import views


urlpatterns = [
    path('', views.labels_list, name='labels-list'),
    path('create/', views.label_create, name='label_create'),
    path('<int:pk>/update/', views.label_update, name='label_update'),
    path('<int:pk>/delete/', views.label_delete, name='label_delete'),
]
