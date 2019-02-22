import datetime, django_filters, requests
from django.db.models import Count
from django.conf import settings

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
    filter_fields = ('movie',)


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
            date__range=(from_date, to_date)
        ).values('movie_id').annotate(
            total_comments=Count('movie')
        ).order_by('-total_comments')

        # Add ranking position to each of the movies
        prev_count, prev_rank_pos = None, 0

        for movie in counted_movie_comments:
            if prev_count != movie['total_comments']:
                prev_rank_pos += 1
                prev_count = movie['total_comments']

            movie['rank'] = prev_rank_pos

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
    filter_fields = ('year', 'director', 'actors', 'language', )
    search_fields = ('title', 'director')
    ordering_fields = ('title', 'year', 'director', 'movie_type')
    ordering = ('year', )

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSerializer
        else:
            return MovieTitleSerializer

    def create(self, request, **kwargs):
        self.serializer_class = MovieTitleSerializer

        if 'title' in request.data:
            # Get title of movie to add to the database
            movie_name = request.data.get('title')

            # Get data about the movie from OMDB API
            payload = {'t': movie_name, 'apikey': settings.OMDB_API_KEY}
            omdb_data = requests.get('https://www.omdbapi.com/', params=payload)
            result = omdb_data.json()

            if Movie.objects.filter(title=result['Title']).exists():
                # If movie was already added to the database get the object and return it
                serializer = MovieSerializer(Movie.objects.filter(title=result['Title']).first())
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Convert results from OMDB into serializer-friendly format
                result = {k.lower(): v for k, v in result.items()}
                result['movie_type'] = result.pop('type')

                for element in result['ratings']:
                    for key, value in element.items():
                        element[key.lower()] = element.pop(key)

                # Initialize the serializer with converted request data
                serializer = MovieSerializer(data=result)

                if serializer.is_valid():
                    # Deserialize data and store in database
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    # Return error if invalid data provided
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Invalid request": request.data}, status=status.HTTP_400_BAD_REQUEST)
