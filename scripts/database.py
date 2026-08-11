from src.db.database import SessionLocal


def get_session():
    return SessionLocal()