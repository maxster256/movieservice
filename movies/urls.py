from django.conf.urls import url
from . import views

from rest_framework.routers import SimpleRouter

from .views import MovieCommentsViewSet, TopListView, MovieViewSet

router = SimpleRouter()
router.register("comments", MovieCommentsViewSet, base_name='comment')
router.register("movies", MovieViewSet, base_name='movies')


urlpatterns = [
    url(r'^top/$', TopListView.as_view(), name='top'),
]

urlpatterns += router.urls
