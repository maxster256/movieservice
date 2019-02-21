import datetime
import json

from django.db.models import Count
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from movies.views import MovieViewSet, MovieCommentsViewSet, TopListView
from ..models import Movie, MovieComment
from ..serializers import MovieSerializer, MovieCommentSerializer, TopSerializer

# Initialize the API Client
client = Client()


class GetAllMoviesTest(TestCase):
    """
    Test module for GET all movies API
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MovieViewSet.as_view({'get': 'list'})

        Movie.objects.create(
            Title='Fight Club', Year='1997', Rated='R', Released='1997', Runtime='120', Genre='Crime',
            Director='David Fincher', Writer='Chuck Palachniuk', Actors='Edward Norton, Brad Pitt',
            Plot='A New-York Yippie Finds Himself In A Very Strange Situation', Language='English',
            Country='US', Awards='Oscars', Poster='fightclub.com/poster.jpg', Metascore='97', imdbRating='9.8',
            imdbVotes='14435', imdbID='19929495', Type='Movie', DVD='1999', BoxOffice='16669649443',
            Production='Sony', Website='fightclub.com', Response='True',
        )

    def test_get_all_movies(self):
        # Get API response
        request = self.factory.get('/movies/')
        response = self.view(request)

        # Get data from the database
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddNewMovieTest(TestCase):
    """
    Test module validating the insertion of new movie into database
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MovieViewSet.as_view({'post': 'create'})

        self.valid_payload = {'Title': 'Fight Club'}
        self.invalid_payload = {'Name': 'Korcev'}

    def test_add_movie_valid_title(self):
        request = self.factory.post('/movies', self.valid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.data['Title'], self.valid_payload['Title'])
        self.assertNotEquals(response.data['Director'], None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_invalid_title(self):
        request = self.factory.post('/movies', self.invalid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllCommentsTest(TestCase):
    """
    Test module validating the GET comments
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MovieCommentsViewSet.as_view({'get': 'list'})

        MovieComment.objects.create(
            CommentedMovieID_id=7, Comment="That was a great one!", Date=datetime.date.today()
        )
        MovieComment.objects.create(
            CommentedMovieID_id=5, Comment="Loved it!", Date=datetime.date.today() - datetime.timedelta(1)
        )

    def test_get_all_comments(self):
        # Get API response
        request = self.factory.get('/comments/')
        response = self.view(request)

        # Get data from the database
        comments = MovieComment.objects.all()
        serializer = MovieCommentSerializer(comments, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AddNewCommentTest(TestCase):
    """
    Test module validating the insertion of new comments into database
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MovieCommentsViewSet.as_view({'post': 'create'})

        Movie.objects.create(
            Title='Fight Club', Year='1997', Rated='R', Released='1997', Runtime='120', Genre='Crime',
            Director='David Fincher', Writer='Chuck Palachniuk', Actors='Edward Norton, Brad Pitt',
            Plot='A New-York Yippie Finds Himself In A Very Strange Situation', Language='English',
            Country='US', Awards='Oscars', Poster='fightclub.com/poster.jpg', Metascore='97', imdbRating='9.8',
            imdbVotes='14435', imdbID='19929495', Type='Movie', DVD='1999', BoxOffice='16669649443',
            Production='Sony', Website='fightclub.com', Response='True',
        )

        self.valid_payload = {'CommentedMovieID': 1, "Comment": 'Loved that one!'}
        self.invalid_payload = {'CommentMovieTitle': 'Killing Me Softly', "CommentContents": 'What a duce?'}

    def test_add_valid_comment(self):
        request = self.factory.post('/comments', self.valid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.data['Comment'], self.valid_payload['Comment'])
        self.assertEqual(response.data['CommentedMovieID'], self.valid_payload['CommentedMovieID'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_invalid_title(self):
        request = self.factory.post('/comments', self.invalid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TopTest(TestCase):
    """
    Test module validating the workings of the Top API view
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = TopListView.as_view()

        Movie.objects.create(
            Title='Fight Club', Year='1997', Rated='R', Released='1997', Runtime='120', Genre='Crime',
            Director='David Fincher', Writer='Chuck Palachniuk', Actors='Edward Norton, Brad Pitt',
            Plot='A New-York Yippie Finds Himself In A Very Strange Situation', Language='English',
            Country='US', Awards='Oscars', Poster='fightclub.com/poster.jpg', Metascore='97', imdbRating='9.8',
            imdbVotes='14435', imdbID='19929495', Type='Movie', DVD='1999', BoxOffice='16669649443',
            Production='Sony', Website='fightclub.com', Response='True',
        )

        MovieComment.objects.create(
            CommentedMovieID_id=1, Comment="That was a great one!", Date=datetime.date.today()
        )
        MovieComment.objects.create(
            CommentedMovieID_id=1, Comment="Loved it!", Date=datetime.date.today() - datetime.timedelta(1)
        )

        Movie.objects.create(
            Title='Chipmunk Club', Year='1997', Rated='R', Released='1997', Runtime='120', Genre='Crime',
            Director='Davio Fincherozo', Writer='Chuck Palachniuk', Actors="Nortonny Nod32, Brat Pitta",
            Plot='A New-York Chippy Finds Itself In A Very Squirky Situation', Language='English',
            Country='US', Awards='Oscars', Poster='chipclub.com/poster.jpg', Metascore='97', imdbRating='9.8',
            imdbVotes='14435', imdbID='19929495', Type='Movie', DVD='1999', BoxOffice='16669649443',
            Production='Samsungaza', Website='chipclub.com', Response='True',
        )

    def test_get_top(self):
        # Get API response
        request = self.factory.get('/top/')
        response = self.view(request)

        # Get data from the database
        # Default date filtering settings (one month from today)
        from_date = datetime.date.today() - datetime.timedelta(30)
        to_date = datetime.date.today()

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

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





