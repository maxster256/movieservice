from django.conf.urls import url
from . import views

from rest_framework.routers import SimpleRouter

from .views import MovieCommentsViewSet, Top

router = SimpleRouter()
router.register("comments", MovieCommentsViewSet, basename='comment')
router.register("top", Top)

urlpatterns = [
    # url(
    #     r'^api/v1/puppies/(?P<pk>[0-9]+)$',
    #     views.get_delete_update_puppy,
    #     name='get_delete_update_puppy'
    # ),
    url(
        r'^movies/$',
        views.movies,
        name='movies'
    )
]

urlpatterns += router.urls
