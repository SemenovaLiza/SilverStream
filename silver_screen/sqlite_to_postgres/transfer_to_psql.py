"""sqlite3 and postgre db authentication"""

import logging
import os
import sqlite3
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Dict, Generator

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

DEFAULT_VALUE = ''

@dataclass
class TimeStampedMixin():
    """Class for representing dates."""
    created_at: datetime = field(default= datetime.now())
    updated_at: datetime = field(default= datetime.now())
    
    class Meta:
        abstract = True


@dataclass
class UUIDMixin():
    """Class for hash-identificator."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    class Meta:        
        abstract = True


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    """Class for person representation."""    
    full_name: str = field(default=DEFAULT_VALUE)


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    """Class for genre representation."""    
    name: str = field(default=DEFAULT_VALUE)
    description: str = field(default=None)
    

@dataclass
class FilmWork(UUIDMixin, TimeStampedMixin):
    """Class for filmwork representation."""
    title: str = field(default=DEFAULT_VALUE)
    description: str = field(default=None)
    creation_date: datetime = field(default=None)
    file_path: str = field(default=None)
    rating: float = field(default=None)
    type: str = field(default=('Movie'))


@dataclass
class GenreFilmWork(UUIDMixin):
    """Class for filmwork's genre representation."""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default=datetime.now())


@dataclass
class PersonFilmWork(UUIDMixin):
    """Class for filmwork's person representation."""    
    role: str = field(default='')
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default=datetime.now())


class SQLiteExtractor:
    """Class for extracting data from sqlite3 db."""
    def __init__(self, conn: sqlite3.Connection):
        self.sql_conn = conn.cursor()
        self.table_name = (
            'person',
            'genre',
            'film_work',
            'genre_film_work',
            'person_film_work'
        )

    def extract_movies(self):
        """Extract data from table."""
        for table_name in self.table_name:
            try:
                self.sql_conn.execute(
                    f"""SELECT * FROM {table_name}"""
                )
                logging.info('slite3 connected')
            except sqlite3.Error as e:
                logging.exception(e)
                break

            while True:
                rows = self.sql_conn.fetchmany(int(os.environ.get('CHUNK_SIZE')))
                if rows:
                    yield (table_name, rows)
                else:
                    break


class PostgresSaver:
    """Class for loading data into postgre bd."""
    def __init__(self, psql_conn: RealDictCursor) -> None:
        self.psql_conn = psql_conn
        self.table_name = (
            'person',
            'genre',
            'film_work',
            'genre_film_work',
            'person_film_work')
        self.default_value = DEFAULT_VALUE

    def insert_query(
            self,
            table_name: str,
            row: Dict) -> None:
        """Inserts data into table."""
        cols = ','.join(row.keys())
        qmarks = ','.join(['%s' for s in row.keys()])
        values = tuple(row.values())
        insert_statement = f"INSERT INTO content.{table_name} ({cols}) VALUES ({qmarks}) ON CONFLICT DO NOTHING;"

        with self.psql_conn.cursor() as cur:
            try:
                cur.execute(insert_statement, values)
                self.psql_conn.commit()
                logging.info('postrgresql commit success')
                logging.info(f'query: {insert_statement}. values: {values}')
            except psycopg2.Error as e:
                logging.exception(e)

    def validate_person(self, row):
        """Person validation."""
        created = Person(
            id=row['id'],
            full_name=self.default_value if row['full_name'] is None \
                else row['full_name'],
            created_at=datetime.now() if row['created_at'] is None else row['created_at'],
            updated_at=datetime.now() if row['updated_at'] is None else row['updated_at']
        )
        
        return created   

    def validate_genre(self, row):
        """Genre validation."""
        created = Genre(
            id=row['id'],
            name=self.default_value if row['name'] is None else row['name'],
            description=row['description'],
            created_at=datetime.now() if row['created_at'] is None else row['created_at'],
            updated_at=datetime.now() if row['updated_at'] is None else row['updated_at']
        )
        
        return created       

    def validate_film_work(self, row):
        """Filmwork validation."""
        created = FilmWork(
            id=row['id'],
            title=self.default_value if row['title'] is None else row['title'],
            description=row['description'],
            creation_date=row['creation_date'],
            file_path=row['file_path'],
            rating=row['rating'],
            type='movie' if row['type'] is None else row['type'],
            created_at=datetime.now() if row['created_at'] is None else row['created_at'],
            updated_at=datetime.now() if row['updated_at'] is None else row['updated_at']
        )
        
        return created     

    def validate_genre_film_work(self, row):
        """Filmwork's genre validation."""
        created = GenreFilmWork(
            id=row['id'],
            film_work_id=row['film_work_id'],
            genre_id=row['genre_id'],
            created_at=datetime.now() if row['created_at'] is None else row['created_at'],
        )
        
        return created   

    def validate_person_film_work(self, row):
        """Filmwork's person validation."""
        created = PersonFilmWork(
            id=row['id'],
            role=row['role'],
            film_work_id=row['film_work_id'],
            person_id=row['person_id'],
            created_at=datetime.now() if row['created_at'] is None else row['created_at'],            
        )   

        return created

    def save_all_data(self, gen: Generator) -> None:
        """Validates data and inserts it into db."""
        for tup in gen:
            table_name, rows = tup
            for row in rows:                
                if table_name == 'person':
                    created = self.validate_person(row) 
                elif table_name == 'genre':
                    created = self.validate_genre(row)                            
                elif table_name == 'film_work':
                    created = self.validate_film_work(row) 
                elif table_name == 'person_film_work':
                    created = self.validate_person_film_work(row)                    
                elif table_name == 'genre_film_work':
                    created = self.validate_genre_film_work(row)
                row_validated = asdict(created)   
                self.insert_query(
                    table_name=table_name,
                    row=row_validated
                )
