from django.urls import path
from . import views

urlpatterns = [
    path('statuses/', views.list_statuses, name='list_statuses'),
    path('require_login/', views.require_login, name='require_login'),
    path('statuses/create/', views.create_status, name='create_status'),
    path('statuses/<int:pk>/update/', views.update_status,
         name='update_status'),
    path('statuses/<int:pk>/delete/', views.delete_status,
         name='delete_status'),

]
