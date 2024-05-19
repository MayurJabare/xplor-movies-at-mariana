from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    
    path('', views.home_page, name='home'),
    
    path('vote/<str:date>/', views.movies_by_date, name='movies_by_date'),
    path('add_vote/', views.vote_for_movie, name='vote_for_movie'),   
]
