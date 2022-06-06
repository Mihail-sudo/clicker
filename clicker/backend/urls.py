from django.contrib import admin
from django.urls import path
from backend import views

boosts = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

lonely_boost = views.BoostViewSet.as_view({
    'put': 'patrial_update'
})

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('boosts/', boosts, name='boosts'),
    path('boost/<int:pk>/', lonely_boost, name='boost'),
    path('call_click/', views.call_click, name='call_click'),
]
