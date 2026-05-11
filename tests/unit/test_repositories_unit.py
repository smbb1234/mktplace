from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.models.common import Base
from src.backend.repositories.leads import LeadsRepository
from src.backend.repositories.sessions import SessionsRepository


def _get_memory_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_leads_repository_create_and_get():
    db = _get_memory_session()
    repo = LeadsRepository(db)
    data = {
        "vehicle_id": "V1",
        "full_name": "Tester",
        "email": "t@example.com",
        "phone": "123",
    }
    e = repo.create_enquiry(enquiry_data=data)
    assert e.enquiry_id is not None
    fetched = repo.get_enquiry(e.enquiry_id)
    assert fetched.enquiry_id == e.enquiry_id


def test_sessions_repository_create_and_get():
    db = _get_memory_session()
    repo = SessionsRepository(db)
    s = repo.create_session()
    assert s.session_id is not None
    fetched = repo.get_session(s.session_id)
    assert fetched.session_id == s.session_id
