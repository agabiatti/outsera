from sqlalchemy.orm import Session
from app.models import Movie, Producer, Studio

class MovieController():
    def __init__(self, db: Session):
        self.db = db

    def create_movie(self, movie):
        db_movie = Movie(**movie.model_dump())
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie
    
    def read_movies(self):
        return self.db.query(Movie).all()
    
    def read_movie(self, movie_id):
        return self.db.get(Movie, movie_id)
    
    def update_movie(self, movie_id, movie):
        db_movie = self.db.get(Movie, movie_id)
        
        if not db_movie:
            return None
        
        for key, value in movie.model_dump().items():
            setattr(db_movie, key, value)
        
        self.db.commit()
        self.db.refresh(db_movie)

        return db_movie
    
    def delete_movie(self, movie_id):
        db_movie = self.db.get(Movie, movie_id)
        
        if not db_movie:
            return False
        
        self.db.delete(db_movie)
        self.db.commit()

        return False
    
    def create_movie_with_associations(self, movie_data):
        producers = []
        for name in movie_data.producers:
            producer = self.db.query(Producer).filter(Producer.name == name).first()
            if not producer:
                producer = Producer(name=name)
                self.db.add(producer)
                self.db.commit()
                self.db.refresh(producer)
            
            producers.append(producer)

        studios = []
        for name in movie_data.studios:
            studio = self.db.query(Studio).filter(Studio.name == name).first()
            if not studio:
                studio = Studio(name=name)
                self.db.add(studio)
                self.db.commit()
                self.db.refresh(studio)
            
            studios.append(studio)

        new_movie = Movie(
            title=movie_data.title,
            release_year=movie_data.release_year,
            winner=movie_data.winner,
            producers=producers,
            studios=studios,
        )

        self.db.add(new_movie)
        self.db.commit()
        self.db.refresh(new_movie)

        return {
            "id": new_movie.id,
            "title": new_movie.title,
            "release_year": new_movie.release_year,
            "winner": new_movie.winner,
            "producers": [p.name for p in new_movie.producers],
            "studios": [s.name for s in new_movie.studios]
        }