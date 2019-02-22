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
            title='Fight Club', year='1997', rated='R', released='1997', runtime='120', genre='Crime',
            director='David Fincher', writer='Chuck Palachniuk', actors='Edward Norton, Brad Pitt',
            plot='A New-York Yippie Finds Himself In A Very Strange Situation', language='English',
            country='US', awards='Oscars', poster='fightclub.com/poster.jpg', metascore='97', imdbrating='9.8',
            imdbvotes='14435', imdbid='19929495', movie_type='Movie', dvd='1999', boxoffice='16669649443',
            production='Sony', website='fightclub.com', response='True',
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

        self.valid_payload = {'title': 'Fight Club'}
        self.invalid_payload = {'Name': 'Korcev'}

    def test_add_movie_valid_title(self):
        request = self.factory.post('/movies', self.valid_payload, format='json')
        response = self.view(request)

        movies = Movie.objects.all()

        self.assertEqual(response.data['title'], self.valid_payload['title'])
        self.assertNotEquals(response.data['director'], None)
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
            commented_movie_id_id=7, comment="That was a great one!", date=datetime.date.today()
        )
        MovieComment.objects.create(
            commented_movie_id_id=5, comment="Loved it!", date=datetime.date.today() - datetime.timedelta(1)
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
            title='Fight Club', year='1997', rated='R', released='1997', runtime='120', genre='Crime',
            director='David Fincher', writer='Chuck Palachniuk', actors='Edward Norton, Brad Pitt',
            plot='A New-York Yippie Finds Himself In A Very Strange Situation', language='English',
            country='US', awards='Oscars', poster='fightclub.com/poster.jpg', metascore='97', imdbrating='9.8',
            imdbvotes='14435', imdbid='19929495', movie_type='Movie', dvd='1999', boxoffice='16669649443',
            production='Sony', website='fightclub.com', response='True',
        )

        self.valid_payload = {'commented_movie_id': 1, "comment": 'Loved that one!'}
        self.invalid_payload = {'CommentMovieTitle': 'Killing Me Softly', "CommentContents": 'What a duce?'}

    def test_add_valid_comment(self):
        request = self.factory.post('/comments', self.valid_payload, format='json')
        response = self.view(request)

        self.assertEqual(response.data['comment'], self.valid_payload['comment'])
        self.assertEqual(response.data['commented_movie_id'], self.valid_payload['commented_movie_id'])
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
            title='Fight Club', year='1997', rated='R', released='1997', runtime='120', genre='Crime',
            director='David Fincher', writer='Chuck Palachniuk', actors='Edward Norton, Brad Pitt',
            plot='A New-York Yippie Finds Himself In A Very Strange Situation', language='English',
            country='US', awards='Oscars', poster='fightclub.com/poster.jpg', metascore='97', imdbrating='9.8',
            imdbvotes='14435', imdbid='19929495', movie_type='Movie', dvd='1999', boxoffice='16669649443',
            production='Sony', website='fightclub.com', response='True',
        )

        MovieComment.objects.create(
            commented_movie_id_id=1, comment="That was a great one!", date=datetime.date.today()
        )
        MovieComment.objects.create(
            commented_movie_id_id=1, comment="Loved it!", date=datetime.date.today() - datetime.timedelta(1)
        )

        Movie.objects.create(
            title='Not a Fight Club', year='1997', rated='R', released='1997', runtime='120', genre='Crime',
            director='David Fincheroza', writer='Chuck Palachniuks', actors='Edward Nortony, Brad Pitt',
            plot='A New-York Yippie Finds Himself In A Very Strange Situation', language='English',
            country='US', awards='Oscars', poster='fightclub.com/poster.jpg', metascore='97', imdbrating='9.8',
            imdbvotes='14435', imdbid='19929495', movie_type='Movie', dvd='1999', boxoffice='16669649443',
            production='Sony', website='fightclub.com', response='True',
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
            date__range=(from_date, to_date)
        ).values('commented_movie_id_id').annotate(
            comments_count=Count('commented_movie_id')
        ).order_by('-comments_count')

        # Add ranking position to each of the movies
        prev_count, prev_rank_pos = None, 0

        for movie in counted_movie_comments:
            if prev_count != movie['comments_count']:
                prev_rank_pos += 1
                prev_count = movie['comments_count']

            movie['rank_position'] = prev_rank_pos

        serializer = TopSerializer(counted_movie_comments, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)





