# api/views.py

import json
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import F, Max, Case, When, Value, IntegerField, OuterRef, Subquery
from django.http import JsonResponse
from app.models import Movie, Genre, Rating, MovieSchedule, UserMovieVote
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes



@api_view(['POST'])
def api_login(request):
    print('Function Called.......')
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        return Response({'token': token.key, 'user': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})



@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # form.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return JsonResponse({'message': 'Registration successful'})
        else:
            errors = json.loads(form.errors.as_json())
            return JsonResponse({'errors': errors}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['GET'])
def home_page(request, search_word=None, genre=None):
    # Use TokenAuthentication for authentication
    all_genres = Genre.objects.all().values_list('name', flat=True)

    max_meta_score_subquery = MovieSchedule.objects.filter(
        date=OuterRef('date')
    ).annotate(
        meta_score=Case(
            When(movie__meta_score='N/A', then=Value(0)),
            default=F('movie__meta_score'),
            output_field=IntegerField()
        )
    ).values('date').annotate(
        max_meta_score=Max('meta_score')
    ).values('max_meta_score')

    highest_meta_score_movies = MovieSchedule.objects.annotate(
        max_meta_score=Subquery(max_meta_score_subquery)
    ).annotate(
        meta_score=Case(
            When(movie__meta_score='N/A', then=Value(0)),
            default=F('movie__meta_score'),
            output_field=IntegerField()
        )
    ).filter(
        meta_score=F('max_meta_score')
    ).select_related('movie').prefetch_related('movie__genres').order_by('date')

    if search_word:
        highest_meta_score_movies = highest_meta_score_movies.filter(movie__title__contains=search_word)

    # Serialize the queryset data into JSON
    movies_data = [
        {
            'date': movie.date,
            'title': movie.movie.title,
            'meta_score': movie.movie.meta_score,
            'poster': movie.movie.poster,
            'imdb_rating': movie.movie.imdb_rating,
            'year': movie.movie.year,
            'runtime': movie.movie.runtime,
            'genres': list(movie.movie.genres.values_list('name', flat=True))
        }
        for movie in highest_meta_score_movies
    ]

    # Return the JSON response
    return JsonResponse({'movies': movies_data, 'all_genres': list(all_genres)}, encoder=DjangoJSONEncoder)



@api_view(['GET'])
def movies_by_date(request, date):
   
    # Parse the date string to datetime object
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    movies = MovieSchedule.objects.filter(date=date_obj)

    movie_list = []
    for movie_schedule in movies:
        movie_data = {
            'id': movie_schedule.pk,
            'movie_id': movie_schedule.movie.pk,
            'title': movie_schedule.movie.title,
            'meta_score': movie_schedule.movie.meta_score,
            'date': str(movie_schedule.date)
        }
        movie_list.append(movie_data)
        
    # Return the serialized JSON response
    return JsonResponse({'date': date, 'movies': movie_list})



@api_view(['GET'])
def vote_for_movie(request):
    if request.method == 'GET':

        movie_id = request.GET['movie_id']
        movie_schedule = MovieSchedule.objects.get(pk=movie_id)

        # Update the Metacritic score
        if movie_schedule.movie.meta_score == 'N/A':
            movie_schedule.movie.meta_score = 1  # Set to 1 since 'N/A' is treated as 0 + 1
        else:
            movie_schedule.movie.meta_score = F('meta_score') + 1  # Increment Metacritic score by 1

        movie_schedule.movie.save()  # Save the updated Metacritic score
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})