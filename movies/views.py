import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils import json

from .models import Movie
from .serializers import MovieSerializer


# @api_view(['GET', 'DELETE', 'PUT'])
# def get_delete_update_puppy(request, pk):
#     try:
#         puppy = Puppy.objects.get(pk=pk)
#     except Puppy.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     # get details of a single puppy
#     if request.method == 'GET':
#         return Response({})
#     # delete a single puppy
#     elif request.method == 'DELETE':
#         return Response({})
#     # update details of a single puppy
#     elif request.method == 'PUT':
#         return Response({})


@api_view(['GET', 'POST'])
def movies(request):
    if request.method == 'GET':
        # Get movies
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Insert new movie
        movie_name = request.data.get('name')
        print("REQUEST BODY: {}".format(movie_name))

        payload = {'t': movie_name, 'apikey': 'b3a374e7'}
        omdb_data = requests.get('https://www.omdbapi.com/', params=payload)

        result = omdb_data.json()
        print(result)

        serializer = MovieSerializer(data=result)

        if serializer.is_valid():
            serializer.save()
            print("SUCCESS!!!")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
