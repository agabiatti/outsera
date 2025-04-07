import csv
import re
from app.models.base import Base
from app.models import Movie, Producer, Studio
from app.connections.db import engine, SessionLocal

def split_multi(value):
    return [item.strip() for item in re.split(r',| and ', value) if item.strip()]

def get_or_create(session, model, name):
    instance = session.query(model).filter_by(name=name).first()

    if not instance:
        instance = model(name=name)
        session.add(instance)
        session.commit()
    
    return instance

def load_data(csv_file):
    try:
        Base.metadata.create_all(bind=engine)
        session = SessionLocal()

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')

            for row in reader:
                instance = session.query(Movie).filter_by(title=row['title']).first()
                    
                if not instance:
                    movie = Movie(
                        release_year=int(row['year']),
                        title=row['title'].strip(),
                        winner=row['winner'].strip().lower() == 'yes'
                    )

                    session.add(movie)

                    for pname in split_multi(row['producers']):
                        producer = get_or_create(session, Producer, pname)
                        movie.producers.append(producer)

                    for sname in split_multi(row['studios']):
                        studio = get_or_create(session, Studio, sname)
                        movie.studios.append(studio)

            session.commit()

        session.close()
        
        return True
    except:
        return False