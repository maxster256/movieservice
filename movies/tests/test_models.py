from django.test import TestCase
from movies.models import Movie
from datetime import datetime


class MovieTest(TestCase):
    """ Test module for Puppy model """

    def setUp(self):
        Movie.objects.create(
            Title='Fight Club', Year='1997', Rated='R', Released='1997', Runtime='120', Genre='Crime',
            Director='David Fincher', Writer='Chuck Palachniuk', Actors='Edward Norton, Brad Pitt',
            Plot='A New-York Yippie Finds Himself In A Very Strange Situation', Language='English',
            Country='US', Awards='Oscars', Poster='fightclub.com/poster.jpg', Metascore='97', imdbRating='9.8',
            imdbVotes='14435', imdbID='19929495', Type='Movie', DVD='1999', BoxOffice='16669649443',
            Production='Sony', Website='fightclub.com', Response='True',
        )

    def test_movie(self):
        fight_club = Movie.objects.get(Title='Fight Club')
        self.assertEqual(fight_club.__repr__(), "Fight Club")

