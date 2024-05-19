
def populate_movies_and_schedules_from_file(request=None):
        for entry in data:
            schedule_date = datetime.strptime(entry['date'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
            for movie_data in entry['movies']:
                movie = Movie.objects.create(
                    title=movie_data['title'],
                    year=movie_data['year'],
                    rated=movie_data['rated'],
                    released=datetime.strptime(movie_data['released'], '%d %b %Y').date(),
                    runtime=movie_data['runtime'],
                    plot=movie_data['plot'],
                    language=movie_data['language'],
                    country=movie_data['country'],
                    awards=movie_data['awards'],
                    poster=movie_data['poster'],
                    meta_score=movie_data['meta_score'],
                    imdb_rating=float(movie_data['imdb_rating']),
                    imdb_votes=int(movie_data['imdb_votes'].replace(',', '')),
                    imdb_id=movie_data['imdb_id'],
                    dvd=datetime.strptime(movie_data['dvd'], '%d %b %Y').date() if movie_data['dvd']!='N/A' else None,
                    box_office=movie_data['box_office'],
                    production=movie_data['production'],
                    website=movie_data['website']
                )

                # Adding genres
                for genre_name in movie_data['genre']:
                    genre, created = Genre.objects.get_or_create(name=genre_name)
                    movie.genres.add(genre)

                # Adding ratings
                for rating_data in movie_data['Ratings']:
                    rating, created = Rating.objects.get_or_create(
                        source=rating_data['source'],
                        value=rating_data['value']
                    )
                    movie.ratings.add(rating)

                # Create MovieSchedule
                movie_schedule, created = MovieSchedule.objects.get_or_create(
                    movie=movie,
                    date=schedule_date
                )
  