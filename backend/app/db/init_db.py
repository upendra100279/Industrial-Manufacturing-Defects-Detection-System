"""
Standalone script to initialize the database schema without starting
the full FastAPI app. Useful for CI or manual setup.
"""
from app.db.base import Base, engine
from app.models import user, inspection, detection  # noqa: F401 ensures models register


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


if __name__ == "__main__":
    init_db()
