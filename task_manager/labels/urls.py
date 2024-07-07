from django.urls import path
from . import views


urlpatterns = [
    path('labels/', views.labels_list, name='labels-list'),
    path('labels/create/', views.label_create, name='label_create'),
    path('labels/<int:pk>/update/', views.label_update, name='label_update'),
    path('labels/<int:pk>/delete/', views.label_delete, name='label_delete'),
]
