from django.urls import path
from .views import room, create, update, delete, deleteMessage, topics


urlpatterns = [
    # room id
    path('<int:pk>/', room, name='room'),

    path('topics/', topics, name='topics'),

    path('create/', create, name='create-room'),
    path('update/<str:pk>', update, name='update-room'),
    path('delete/<str:pk>', delete, name='delete-room'),

    path('delete-message/<str:pk>', deleteMessage, name='delete-message'),
]
