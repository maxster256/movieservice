from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Movie, MovieRating


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

    # def create(self, validated_data):
    #     print("Ratings data: {}".format(validated_data))
    #
    #     ratings_data = validated_data.pop('Ratings')
    #
    #     movie = Movie.objects.create(**validated_data)
    #
    #     for rating_data in ratings_data:
    #         MovieRating.objects.create(Movie=movie, **rating_data)
    #
    #     return movie
