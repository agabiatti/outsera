import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.controllers.studio_controller import StudioController
from app.schemas.studio_schema import StudioCreate

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_studio(db_session):
    controller = StudioController(db_session)
    studio_data = StudioCreate(name="Studio 1")
    studio = controller.create_studio(studio_data)

    assert studio.id is not None
    assert studio.name == "Studio 1"


def test_read_studios(db_session):
    controller = StudioController(db_session)
    controller.create_studio(StudioCreate(name="Studio 2"))
    controller.create_studio(StudioCreate(name="Studio 3"))

    studios = controller.read_studios()
    assert len(studios) == 2


def test_update_studio(db_session):
    controller = StudioController(db_session)
    studio = controller.create_studio(StudioCreate(name="Studio Old"))

    updated = controller.update_studio(studio.id, StudioCreate(name="Studio New"))

    assert updated is not None
    assert updated.name == "Studio New"


def test_delete_studio(db_session):
    controller = StudioController(db_session)
    studio = controller.create_studio(StudioCreate(name="Studio Deleted"))

    result = controller.delete_studio(studio.id)
    assert result is True

    assert controller.read_studio(studio.id) is None