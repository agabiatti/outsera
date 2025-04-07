import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.controllers.movie_controller import MovieController
from app.schemas.movie_schema import MovieCreate, MovieFullCreate

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def controller(db):
    return MovieController(db)

def test_create_movie(controller):
    movie_data = MovieCreate(
        title="Test Movie",
        release_year=2022,
        winner=False
    )
    movie = controller.create_movie(movie_data)
    assert movie.id is not None
    assert movie.title == "Test Movie"

def test_read_movies(controller):
    controller.create_movie(MovieCreate(title="A", release_year=2000, winner=True))
    controller.create_movie(MovieCreate(title="B", release_year=2001, winner=False))
    movies = controller.read_movies()
    assert len(movies) == 2

def test_read_movie(controller):
    movie = controller.create_movie(MovieCreate(title="Test Movie2", release_year=2021, winner=True))
    result = controller.read_movie(movie.id)
    assert result.title == "Test Movie2"

def test_update_movie(controller):
    movie = controller.create_movie(MovieCreate(title="Old Movie", release_year=2010, winner=False))
    updated = controller.update_movie(movie.id, MovieCreate(title="New Movie", release_year=2015, winner=True))
    assert updated.title == "New Movie"
    assert updated.winner is True

def test_delete_movie(controller):
    movie = controller.create_movie(MovieCreate(title="Movie To Delete", release_year=2005, winner=False))
    result = controller.delete_movie(movie.id)
    assert result is False
    assert controller.read_movie(movie.id) is None

def test_create_movie_with_associations(controller):
    movie_data = MovieFullCreate(
        title="Test Movie3",
        release_year=2023,
        winner=True,
        producers=["Producer A", "Producer B"],
        studios=["Studio X", "Studio Y"]
    )

    result = controller.create_movie_with_associations(movie_data)
    assert result["title"] == "Test Movie3"
    assert set(result["producers"]) == {"Producer A", "Producer B"}
    assert set(result["studios"]) == {"Studio X", "Studio Y"}