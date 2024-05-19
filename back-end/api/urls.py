# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.api_login, name='api_login'),
    path('logout/', views.logout_view, name='api_logout'),
    path('register/', views.register_view, name='api_register'),
    path('home/', views.home_page, name='api_home'),
    path('movies_by_date/<str:date>/', views.movies_by_date, name='api_movies_by_date'),
    path('vote/', views.vote_for_movie, name='api_vote'),
]
