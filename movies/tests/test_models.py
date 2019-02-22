from django.test import TestCase
from movies.models import Movie
from datetime import datetime


class MovieTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Movie.objects.create(
            title='Fight Club', year='1997', rated='R', released='1997', runtime='120', genre='Crime',
            director='David Fincher', writer='Chuck Palachniuk', actors='Edward Norton, Brad Pitt',
            plot='A New-York Yippie Finds Himself In A Very Strange Situation', language='English',
            country='US', awards='Oscars', poster='fightclub.com/poster.jpg', metascore='97', imdbrating='9.8',
            imdbvotes='14435', imdbid='19929495', movie_type='Movie', dvd='1999', boxoffice='16669649443',
            production='Sony', website='fightclub.com', response='True',
        )

    def test_movie(self):
        fight_club = Movie.objects.get(title='Fight Club')
        self.assertEqual(fight_club.__repr__(), "Fight Club")

