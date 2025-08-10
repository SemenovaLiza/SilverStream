from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MoviesViewSet

router = DefaultRouter()
router.register('movies', MoviesViewSet, basename='movies')
urlpatterns = [path('', include(router.urls))]