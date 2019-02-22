# movieservice

`movieservice` is a simple REST API web service that provides access to detailed information about movies downloaded 
from `OMDB API`.

It also allows users to add comments about movies added to the database as well as see the ranking of top movies, 
where position is determined by number of comments made to each movie.

## API

The API documentation is available [via Postman](https://documenter.getpostman.com/view/4296094/S11ExM3C).

## Additional features

List of movies can be filtered, sorted and searched through via API calls or generated browsable API view.

## Depedencies

The excellent `Django Rest Framework` was used due to the number of powerful features provided for the user, including:
- Serializers, which allow for easy model querysets/instances validation and conversion to native datatypes
- Browsable API, providing approachable interface for interacting with API

`django_filters` were also used to provide the filtering capability, and `WritableNestedModelSerializer` helped with 
handling the response from `OMDB API`. Excellent `requests` helped to get the data from `OMDB API`.

## Check it out!

The project is available live at

