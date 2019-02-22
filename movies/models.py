from django.db import models


class Movie(models.Model):
    """
    Stores a single movie entry.
    """
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    rated = models.CharField(max_length=255)
    released = models.CharField(max_length=255)
    runtime = models.CharField(max_length=255)

    genre = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=1024)
    actors = models.CharField(max_length=255)

    plot = models.TextField()

    language = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    awards = models.TextField()

    poster = models.CharField(max_length=255)

    metascore = models.CharField(max_length=255)
    imdbrating = models.CharField(max_length=255)
    imdbvotes = models.CharField(max_length=255)
    imdbid = models.CharField(max_length=255)

    movie_type = models.CharField(max_length=255)
    dvd = models.CharField(max_length=255)
    boxoffice = models.CharField(max_length=255)
    production = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    response = models.CharField(max_length=255)

    def __repr__(self):
        return self.title


class MovieRating(models.Model):
    ratings = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    source = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class MovieComment(models.Model):
    commented_movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='commented_movie_id')
    comment = models.TextField()
    date = models.DateField(auto_now=True, editable=False)
