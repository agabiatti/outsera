from sqlalchemy.orm import Session, joinedload
from app.models.movie import Movie
from app.models.producer import Producer
from collections import defaultdict

class ProducerController():
    def __init__(self, db: Session):
        self.db = db

    def create_producer(self, producer):
        db_producer = Producer(**producer.model_dump())
        self.db.add(db_producer)
        self.db.commit()
        self.db.refresh(db_producer)
        return db_producer
    
    def read_producers(self):
        return self.db.query(Producer).all()
    
    def read_producer(self, producer_id):
        return self.db.get(Producer, producer_id)
    
    def update_producer(self, producer_id, producer):
        db_producer = self.db.get(Producer, producer_id)
        
        if not db_producer:
            return None
        
        for key, value in producer.model_dump().items():
            setattr(db_producer, key, value)
        
        self.db.commit()
        self.db.refresh(db_producer)

        return db_producer
    
    def delete_producer(self, producer_id):
        db_producer = self.db.get(Producer, producer_id)
        
        if not db_producer:
            return False
        
        self.db.delete(db_producer)
        self.db.commit()

        return True
    
    def get_producer_intervals(self):
        data = defaultdict(list)

        producers = (
            self.db.query(Producer)
            .join(Producer.movies)
            .filter(Movie.winner == True)
            .options(joinedload(Producer.movies))
            .all()
        )

        for producer in producers:
            winning_years = sorted([
                movie.release_year for movie in producer.movies if movie.winner
            ])
            for i in range(1, len(winning_years)):
                data[producer.name].append((winning_years[i-1], winning_years[i]))

        intervals = []
        for producer, wins in data.items():
            for prev_win, next_win in wins:
                if next_win - prev_win > 0:
                    intervals.append({
                        "producer": producer,
                        "interval": next_win - prev_win,
                        "previousWin": prev_win,
                        "followingWin": next_win,
                    })

        if not intervals:
            return {"min": [], "max": []}

        min_val = min(intervals, key=lambda x: x['interval'])['interval']
        max_val = max(intervals, key=lambda x: x['interval'])['interval']

        return {
            "min": [i for i in intervals if i['interval'] == min_val],
            "max": [i for i in intervals if i['interval'] == max_val],
        }