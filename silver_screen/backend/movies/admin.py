"""Admin Panel"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Class for representing a genre in the admin panel.
    ...
    Attributes
    ----------
    list_display : tuple
        fields to display
    """
    list_display = ('name', 'description', 'updated_at')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Class for representing a person in the admin panel.
    ...
    Attributes
    ----------
    list_display : tuple
        fields to display
    """
    list_display = ('full_name', 'updated_at')


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    """
    Class for representing a film work with genres and persons in the admin panel.
    ...
    Attributes
    ----------
    inlines : tuple
        inline classes
    list_display : tuple
        fields to display
    list_filter : tuple
        fields for filtering
    search_fields : tuple
        fields for searching
    """
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline,)
    list_display = ('title', 'description', 'type', 'rating', 'creation_date', 'created_at', 'updated_at')
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')