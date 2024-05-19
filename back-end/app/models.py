from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    source = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.source}: {self.value}"

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4, null=True, blank=True)
    rated = models.CharField(max_length=20, null=True, blank=True)
    released = models.DateField(null=True, blank=True)
    runtime = models.CharField(max_length=10, null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    awards = models.TextField(null=True, blank=True)
    poster = models.URLField(null=True, blank=True)
    meta_score = models.CharField(max_length=20, null=True, blank=True, default='0')
    imdb_rating = models.FloatField(null=True, blank=True)
    imdb_votes = models.IntegerField(null=True, blank=True)
    imdb_id = models.CharField(max_length=20, null=True, blank=True)
    dvd = models.DateField(null=True, blank=True)
    box_office = models.CharField(max_length=50, null=True, blank=True)
    production = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    genres = models.ManyToManyField(Genre)
    ratings = models.ManyToManyField(Rating)

    def __str__(self):
        return self.title

class MovieSchedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.movie.title} on {self.date}"


class UserMovieVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_schedule = models.ForeignKey(MovieSchedule, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} voted for {self.movie_schedule.movie.title} on {self.movie_schedule.date}"