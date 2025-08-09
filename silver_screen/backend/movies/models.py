"""Django admin panel models"""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex

class TimeStampedMixin(models.Model):
    """Class for representing dates.
    ...
    Attributes
    ----------
    created_at : datetime
        creation date
    updated_at : datetime
        update date
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = _('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name = _('Updated at'))

    class Meta:
        abstract = True

    
class UUIDMixin(models.Model):
    """Class for hash identifier
    ...
    Attributes
    ----------
    id : str
        identifier
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='Id')
    
    class Meta:
        abstract = True

        
class Genre(UUIDMixin, TimeStampedMixin):
    """
    Class for representing a genre. Inherits from TimeStampedMixin and UUIDMixin.
    ...
    Attributes
    ----------
    name : str
        genre name
    description : str
        genre description
    """
    name = models.CharField(
        max_length=255,
        default='',
        verbose_name = _('Name')
    )
    description = models.TextField(
        verbose_name = _('Description'),
        null=True,
        default=''
    )

    def __str__(self):
        """Showing genre name"""
        return str(self.name)
    
    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(UUIDMixin, TimeStampedMixin):
    """
    Class for representing a person. Inherits from TimeStampedMixin and UUIDMixin.
    ...
    Attributes
    ----------
    full_name : str
        full name
    """
    full_name = models.CharField(
        max_length=255,
        default='',
        verbose_name = _('Full Name')
    )

    def __str__(self):
        """Showing person's full name"""
        return str(self.full_name)
    
    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    
class FilmWork(UUIDMixin, TimeStampedMixin):
    """
    Class for representing a film work. Inherits from TimeStampedMixin and UUIDMixin.
    ...
    Attributes
    ----------
    title : str
        title
    description : str
        description
    creation_date : datetime
        creation date
    file_path : str
        file path
    rating : float
        rating
    type : str
        type
    """

    # Enumerated Class
    class FilmType(models.TextChoices):
        """
        Class for representing the type of a film work.
        ...
        Attributes
        ----------
        movie : str
            movie
        tv_show : str
            TV show
        """
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'TV_show', _('TV_show')
    
    # FilmWork fields
    title = models.CharField(
        max_length=255,        
        default='', 
        verbose_name = _('Title'),
    )
    description = models.TextField(
        null=True, 
        verbose_name = _('Description')      
    )
    creation_date = models.DateField(         
         verbose_name = _('Creation Date'),
         null=True,
         default=''
    )
    file_path = models.FileField(
        name = 'file_path',
        upload_to='film_works/',
        blank=True, null=True,
        verbose_name = _('FilePath')
    )
    rating = models.FloatField(        
        null=True,        
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
        verbose_name = _('Rating')
    )
    type = models.CharField(        
        max_length=25,
        choices=FilmType.choices,        
        default=FilmType.MOVIE,
        verbose_name = _('Type')      
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persones = models.ManyToManyField(Person, through='PersonFilmWork')

    def __str__(self):
        return str(self.title)

    class Meta:        
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')


class GenreFilmWork(UUIDMixin):
    """
    Class for representing a film work genre. Inherits from UUIDMixin.
    ...
    Attributes
    ----------
    film_work_id : str
        film work identifier
    genre_id : str
        genre identifier
    created_at : datetime
        creation date
    """
    film_work_id = models.ForeignKey(
        'FilmWork',
        on_delete=models.CASCADE,
        db_column='film_work_id',
        verbose_name = _('FilmWork')
    )
    genre_id = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        db_column='genre_id',
        verbose_name = _('Genre')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = _('Created at') )

    class Meta:
        indexes = [
            UniqueIndex(fields=['film_work_id', 'genre_id'])
        ]
        db_table = "content\".\"genre_film_work"
        verbose_name = _('GenreFilmWork')
        verbose_name_plural = _('GenreFilmWorks')


class PersonFilmWork(UUIDMixin):
    """
    Class for representing a film work person. Inherits from UUIDMixin.
    ...
    Attributes
    ----------
    film_work_id : str
        film work identifier
    person_id : str
        person identifier
    role : str
        role
    """
    film_work_id = models.ForeignKey(
        'FilmWork',
        on_delete=models.CASCADE,
        db_column='film_work_id',
        verbose_name = _('FilmWork')
    )
    person_id = models.ForeignKey(
        'Person',
        db_column='person_id',
        on_delete=models.CASCADE,
        verbose_name = _('Person')
    )
    role = models.TextField(verbose_name = _('Role'), default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = _('Created at'))

    class Meta:        
        indexes = [
            UniqueIndex(fields=['film_work_id', 'person_id', 'role']),
        ]
        db_table = "content\".\"person_film_work"
        verbose_name = _('PersonFilmWork')
        verbose_name_plural = _('PersonFilmWorks')