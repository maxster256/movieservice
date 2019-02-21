import datetime

import django_filters
import requests
from django.db.models import Count, Prefetch

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.views import APIView

from .models import Movie, MovieComment
from .serializers import MovieSerializer, MovieCommentSerializer, TopSerializer


class MovieCommentsViewSet(viewsets.ModelViewSet):
    queryset = MovieComment.objects.all()
    serializer_class = MovieCommentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('CommentedMovieID',)


class Top(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = TopSerializer

    def get_queryset(self):
        # Returns number of comments for each movie ID in descending order
        counted_movie_comments = MovieComment.objects.filter(
            Date__range=(datetime.date(2019, 2, 20), datetime.date(2019, 2, 21))
        ).values('CommentedMovieID_id').annotate(
            CommentsCount=Count('CommentedMovieID')
        ).order_by('-CommentsCount')

        # Add ranking position to each of the movies
        prev_count, prev_rank_pos = None, 0

        for movie in counted_movie_comments:

            if prev_count != movie['CommentsCount']:
                prev_rank_pos += 1
                prev_count = movie['CommentsCount']

            movie['RankPosition'] = prev_rank_pos

        return counted_movie_comments


@api_view(['GET', 'POST'])
def movies(request):
    if request.method == 'GET':
        # Get movies
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Insert new movie

        print("REQUEST DATA: {}".format(request.data))

        if 'title' in request.data:
            movie_name = request.data.get('title')

            payload = {'t': movie_name, 'apikey': 'b3a374e7'}
            omdb_data = requests.get('https://www.omdbapi.com/', params=payload)
            result = omdb_data.json()

            serializer = MovieSerializer(data=result)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Invalid request": request.data}, status=status.HTTP_400_BAD_REQUEST)
