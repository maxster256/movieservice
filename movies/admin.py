from django.contrib import admin
from .models import Movie, MovieRating

# Register your models here.
admin.site.register(Movie)
admin.site.register(MovieRating)