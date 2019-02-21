from django.db import models


class Movie(models.Model):
    """
    Stores a single movie entry.
    """
    Title = models.CharField(max_length=255)
    Year = models.CharField(max_length=4)
    Rated = models.CharField(max_length=5)
    Released = models.CharField(max_length=255)
    Runtime = models.CharField(max_length=12)

    Genre = models.CharField(max_length=255)
    Director = models.CharField(max_length=255)
    Writer = models.CharField(max_length=1024)
    Actors = models.CharField(max_length=255)

    Plot = models.TextField()

    Language = models.CharField(max_length=255)
    Country = models.CharField(max_length=255)
    Awards = models.TextField()

    Poster = models.CharField(max_length=255)

    Metascore = models.CharField(max_length=3)
    imdbRating = models.CharField(max_length=4)
    imdbVotes = models.CharField(max_length=255)
    imdbID = models.CharField(max_length=255)

    Type = models.CharField(max_length=255)
    DVD = models.CharField(max_length=255)
    BoxOffice = models.CharField(max_length=255)
    Production = models.CharField(max_length=255)
    Website = models.CharField(max_length=255)
    Response = models.CharField(max_length=255)

    def __repr__(self):
        return self.Title

    # def __str__(self):
    #     return self.Title


class MovieRating(models.Model):
    Ratings = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='Ratings')
    Source = models.CharField(max_length=255)
    Value = models.CharField(max_length=255)


class MovieComment(models.Model):
    CommentedMovieID = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='CommentedMovieID')
    Comment = models.TextField()
    Date = models.DateField(auto_now=True, editable=False)
