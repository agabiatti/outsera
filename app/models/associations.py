from sqlalchemy import Table, Column, ForeignKey
from app.models.base import Base

movie_producers = Table(
    'movie_producers', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('producer_id', ForeignKey('producers.id'), primary_key=True)
)

movie_studios = Table(
    'movie_studios', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('studio_id', ForeignKey('studios.id'), primary_key=True)
)