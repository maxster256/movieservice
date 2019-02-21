from django.conf.urls import url
from . import views

from rest_framework.routers import SimpleRouter

from .views import MovieCommentsViewSet, TopListView, MovieViewSet

router = SimpleRouter()
router.register("comments", MovieCommentsViewSet, basename='comment')
router.register("movies", MovieViewSet, basename='movies')


urlpatterns = [
    # url(
    #     r'^api/v1/puppies/(?P<pk>[0-9]+)$',
    #     views.get_delete_update_puppy,
    #     name='get_delete_update_puppy'
    # ),
    # url(
    #     r'^movies/$',
    #     views.movies,
    #     name='movies'
    # ),
    url(r'^top/$', TopListView.as_view(), name='top'),
    # url(r'^movies/$', MovieListCreateView.as_view(), name='movie')
]

urlpatterns += router.urls
