from django.contrib import admin
from .models import Movie, MovieSchedule, Genre, Rating, UserMovieVote


admin.site.register(Movie)
admin.site.register(MovieSchedule)
admin.site.register(Genre)
admin.site.register(Rating)
admin.site.register(UserMovieVote)