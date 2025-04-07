from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.associations import movie_producers, movie_studios

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    release_year = Column(Integer)
    title = Column(String, unique=True)
    winner = Column(Boolean)

    producers = relationship("Producer", secondary=movie_producers, back_populates="movies")
    studios = relationship("Studio", secondary=movie_studios, back_populates="movies")