from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Movie, MovieRating, MovieComment


class TopSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField()
    rank_position = serializers.IntegerField()
    # Date = serializers.DateField()

    class Meta:
        model = MovieComment
        fields = ('commented_movie_id_id', 'rank_position', 'comments_count')


class MovieCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieComment
        fields = ('commented_movie_id', 'comment', 'date')


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
