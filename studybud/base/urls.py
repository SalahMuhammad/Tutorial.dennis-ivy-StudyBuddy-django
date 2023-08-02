from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('profile/<str:pk>', views.profile, name='user-profile'),

    path('update-user/', views.updateUser, name='update-user'),

    path('activities/', views.activities, name='activities'),
]
