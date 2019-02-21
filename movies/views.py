import datetime, django_filters, requests
from django.db.models import Count

from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework import filters

from .models import Movie, MovieComment
from .serializers import MovieSerializer, MovieCommentSerializer, TopSerializer, MovieTitleSerializer


class MovieCommentsViewSet(viewsets.ModelViewSet):
    """
    get:
    Returns list of comments added. May be filtered by ID of a movie.

    post:
    Adds a new comment for a specified movie ID with given comment's contents.
    """
    queryset = MovieComment.objects.all()
    serializer_class = MovieCommentSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('CommentedMovieID',)


class TopListView(generics.ListAPIView):
    """
    get:
    Returns the ranking of top movies based on number of comments made by users in a given time interval.
    Time interval defaults to 30 days from now if not given via request.
    """
    queryset = Movie.objects.all()
    serializer_class = TopSerializer

    def get(self, request, **kwargs):
        # Default date filtering settings (one month from today)
        from_date = datetime.date.today() - datetime.timedelta(30)
        to_date = datetime.date.today()

        if 'from_date' in request.query_params and 'to_date' in request.query_params:
            # Perform necessary date conversions for query
            from_date = datetime.datetime.strptime(request.query_params.get('from_date', ), '%Y-%m-%d')
            to_date = datetime.datetime.strptime(request.query_params.get('to_date', ), '%Y-%m-%d')

        # Returns number of comments for each movie ID in descending order
        counted_movie_comments = MovieComment.objects.filter(
            Date__range=(from_date, to_date)
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

        serializer = TopSerializer(counted_movie_comments, many=True)
        return Response(serializer.data)


class MovieViewSet(viewsets.ModelViewSet):
    """
    get:
    Returns a list of movies stored in the database with implemented filtering, sorting and search.

    post:
    Adds new movie to the database by reading the title from the request and downloading data from OMDB.
    """

    queryset = Movie.objects.all()

    # Defines filters used for the view
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('Year', 'Rated', 'Director', 'Actors', 'Language', 'Type')
    search_fields = ('Title', 'Director')
    ordering_fields = ('Title', 'Year', 'Director')
    ordering = ('Year',)

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSerializer
        else:
            return MovieTitleSerializer

    def create(self, request, **kwargs):
        self.serializer_class = MovieTitleSerializer

        if 'Title' in request.data:
            movie_name = request.data.get('Title', )

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
