from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Q
from django.db.models.functions import Coalesce
from movies.models import FilmWork
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .serializers import MoviesListSerializer


class PaginationMovies(PageNumberPagination):
    """
    This is a class for pagination movies.
      
    Attributes:
        page_size             (int): Max number of elements on the page
        page_size_query_param (int): Query param for page size
        max_page_size         (int): Max number of pages   
        page_query_param      (str): Verbose name
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
    page_query_param = 'page'


class MoviesViewSet(viewsets.ReadOnlyViewSet):
    """
    This is a class for Movies. Inheritates Filmwork, PaginationMovies, MoviesListSerializer.
      
    Attributes:
        model            (class): Django model class
        pagination_class (class): Paginator class
        serializer_class (class): Serializer class 
    """
    model = FilmWork
    pagination_class = PaginationMovies
    serializer_class = MoviesListSerializer

    def get_queryset(self):
        """
        The function to nuild django rest queryset.
        """
        queryset = self.model.objects.values('id', 'title', 'description', 'creation_date', 'type').annotate(
            rating = Coalesce(F('rating'), 0.0),
            genres = ArrayAgg('genres__name', distinct=True, default=list()),
            actors = ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role='actor'), default=list()),
            directors=ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role='director'), default=list()),
            writers=ArrayAgg('persons__full_name', distinct=True, filter=Q(filmworkperson__role='writer'), default=list())
        )

        return queryset
