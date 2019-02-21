import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Movie
from ..serializers import MovieSerializer


# Initialize the API Client
client = Client()

class GetAllMoviesTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        Movie.objects.create(
            title="Fight Club", year="1997", rated="R", released="20 Oct 1997", runtime=120,
            genre="Crime",
            director="David Fincher", writer="Chuck Palachniuk", actors="Edward Norton, Brad Pitt",
            plot="A yippie finds himself in a strange life situation", language="EN", country="US", awards="Oscars",
            poster="fightclub.com/poster.jpg", metascore=95, rating="[{'imdb': '7/10'}, {'usdaily: 8/10'}]",
            imdb_rating="8.8", imdb_votes="NA", imdb_id="1000001", movie_type="NA", DVD="NA", box_office='NA',
            production="US", website="fightclub.com")

        Movie.objects.create(
            title="Social Network", year="2010", rated="R", released="20 Oct 2010", runtime=120,
            genre="Crime",
            director="David Fincher", writer="Aaron Sorkin", actors="Jesse Eisenberg",
            plot="A Harvard student invents the world's social network", language="EN", country="US", awards="Oscars",
            poster="socialnetwork.com/poster.jpg", metascore=95, rating="[{'imdb': '7/10'}, {'usdaily: 8/10'}]",
            imdb_rating="8.8", imdb_votes="NA", imdb_id="1000001", movie_type="NA", DVD="NA", box_office='NA',
            production="US", website="socialnetwork.com")

    def test_get_all_movies(self):
        # get API response
        response = client.get(reverse('movies'))
        # get data from db
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
