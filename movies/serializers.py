from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Movie, MovieRating, MovieComment


class TopSerializer(serializers.ModelSerializer):
    total_comments = serializers.IntegerField()
    rank = serializers.IntegerField()
    # Date = serializers.DateField()

    class Meta:
        model = MovieComment
        fields = ('movie_id', 'rank', 'total_comments')


class MovieCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieComment
        fields = ('movie', 'comment', 'date')


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ('source', 'value')


class MovieSerializer(WritableNestedModelSerializer):
    ratings = MovieRatingSerializer(many=True, allow_null=True)

    class Meta:
        model = Movie
        fields = ('title', 'year', 'rated', 'released', 'runtime', 'genre', 'director', 'writer', 'actors', 'plot',
                  'language', 'country', 'awards', 'poster', 'metascore', 'ratings', 'imdbrating', 'imdbvotes',
                  'imdbid', 'movie_type', 'dvd', 'boxoffice', 'production', 'website', 'response')


class MovieTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', )
