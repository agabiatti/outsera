import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.controllers.producer_controller import ProducerController
from app.models import Producer, Movie
from app.schemas.producer_schema import ProducerCreate

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def controller(db_session):
    return ProducerController(db=db_session)

def test_create_producer(controller):
    producer = ProducerCreate(name="Teste Producer")
    created = controller.create_producer(producer)
    assert created.name == "Teste Producer"
    assert created.id is not None


def test_read_producers(controller):
    controller.create_producer(ProducerCreate(name="Teste Producer2"))
    producers = controller.read_producers()
    assert len(producers) == 1
    assert producers[0].name == "Teste Producer2"


def test_read_producer(controller):
    created = controller.create_producer(ProducerCreate(name="Teste Producer3"))
    found = controller.read_producer(created.id)
    assert found is not None
    assert found.name == "Teste Producer3"


def test_update_producer(controller):
    created = controller.create_producer(ProducerCreate(name="Producer Old"))
    updated = controller.update_producer(created.id, ProducerCreate(name="Producer New"))
    assert updated.name == "Producer New"


def test_delete_producer(controller):
    created = controller.create_producer(ProducerCreate(name="Teste Producer Delete"))
    deleted = controller.delete_producer(created.id)
    assert deleted is True
    assert controller.read_producer(created.id) is None


def test_get_producer_intervals(controller, db_session):
    producer = Producer(name="Test Producer")
    db_session.add(producer)
    db_session.commit()
    
    movie1 = Movie(title="Movie 1", release_year=2000, winner=True, producers=[producer])
    movie2 = Movie(title="Movie 2", release_year=2010, winner=True, producers=[producer])
    db_session.add_all([movie1, movie2])
    db_session.commit()

    intervals = controller.get_producer_intervals()
    assert "min" in intervals
    assert "max" in intervals
    assert intervals["min"][0]["interval"] == 10
    assert intervals["min"][0]["producer"] == "Test Producer"
