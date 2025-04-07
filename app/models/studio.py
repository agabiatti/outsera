from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.associations import movie_studios

class Studio(Base):
    __tablename__ = "studios"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    movies = relationship("Movie", secondary=movie_studios, back_populates="studios")
