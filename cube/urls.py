from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cube/', views.cube, name='cube'),
    path('chess/', views.cchess, name='chess'),
    path('chess/nextMoveSunFish/', views.nextMoveSunFish , name='nextMoveSunFish'),
    path('test/', views.test , name='nextMove'),
    
]