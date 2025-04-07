from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.associations import movie_producers

class Producer(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    movies = relationship("Movie", secondary=movie_producers, back_populates="producers")