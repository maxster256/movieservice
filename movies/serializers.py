from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Movie, MovieRating, MovieComment


class TopSerializer(serializers.ModelSerializer):
    CommentsCount = serializers.IntegerField()
    RankPosition = serializers.IntegerField()
    # Date = serializers.DateField()

    class Meta:
        model = MovieComment
        fields = ('CommentedMovieID_id', 'RankPosition', 'CommentsCount')


class MovieCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieComment
        fields = ('CommentedMovieID', 'Comment', 'Date')


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ('Source', 'Value')


class MovieSerializer(WritableNestedModelSerializer):
    Ratings = MovieRatingSerializer(many=True, allow_null=True)

    class Meta:
        model = Movie
        fields = ('Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 'Actors', 'Plot',
                  'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'Ratings', 'imdbRating', 'imdbVotes',
                  'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Response')
