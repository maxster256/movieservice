from django.test import TestCase
from movies.models import Movie
from datetime import datetime


class MovieTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Movie.objects.create(
            title="Fight Club", year="1997", rated="R", released="20 Oct 1997", runtime=120,
            genre="Crime",
            director="David Fincher", writer="Chuck Palachniuk", actors="Edward Norton, Brad Pitt",
            plot="A yippie finds himself in a strange life situation", language="EN", country="US", awards="Oscars",
            poster="fightclub.com/poster.jpg", metascore=95, rating="[{'imdb': '7/10'}, {'usdaily: 8/10'}]",
            imdb_rating="8.8", imdb_votes="NA", imdb_id="1000001", movie_type="NA", DVD="NA", box_office='NA',
            production="US", website="fightclub.com"
        )

    def test_movie(self):
        fight_club = Movie.objects.get(title='Fight Club')
        self.assertEqual(fight_club.__repr__(), "Fight Club")

