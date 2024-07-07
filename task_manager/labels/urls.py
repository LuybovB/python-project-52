from django.urls import path
from .views import labels_list, label_create, label_update, label_delete

app_name = 'labels'

urlpatterns = [
    path('', labels_list, name='list'),
    path('create/', label_create, name='create'),
    path('<int:pk>/update/', label_update, name='update'),
    path('<int:pk>/delete/', label_delete, name='delete'),
]
